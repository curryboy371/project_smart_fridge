export default {
	getModules: async () => {
		const modules = await fetchModules.run();

		return modules.map(m => {
			return {
				Id: m.id,
				Name: m.name,
				Duration: m.duration,
				Description: m.description,
				CourseId: m.course_id,
				SubjectId: m.course_subject_id,
			}
		})
	},

	activeModule: {},
	activeModuleContent: {},
	markComplete: null,

	setMarkComplete: (markComplete) => {
		this.markComplete = markComplete;
	},

	setActiveModule: (activeModule) => {
		this.activeModule = activeModule
	},

	setActiveModuleContent: async (activeModuleContent) => {
		const contentType = activeModuleContent.type;
		let content;

		const moduleContent = await fetchOneCourseModuleContent.run({
			id: activeModuleContent.id
		});

		if (contentType === 'Reading Material') {
			content = await fetchReadingContent.run({id: activeModuleContent.id});
		}
		if (contentType === 'Video') {
			content = await fetchVideoContent.run({id: activeModuleContent.id});
		}
		if (contentType === 'Quiz') {
			const quiz = await fetchQuizContent.run({id: activeModuleContent.id});
			const quizQuestions = await fetchQuizQuestions.run({quizId: quiz[0].id});
			content = [{
				...quiz[0],
				questions: quizQuestions
			}]
		}
		this.activeModuleContent = {
			activeModuleContent: moduleContent && moduleContent.length > 0 ? moduleContent.map(c => {
				return {
					id: c.id,
					type: c.content_type,
					name: c.title,
					markComplete: c.mark_complete,
					comment: c.comment
				}
			})[0] : undefined,
			content: content.length > 0 ? content[0] : undefined,
		}
	},

	acceptRejectModuleContent: async () => {
		console.log('MC:', utils.markComplete, utils.activeModuleContent.activeModuleContent);
		await patchModuleContent.run();
		await this.getModules();
		this.setActiveModuleContent(this.activeModuleContent.activeModuleContent);
		showAlert('Module Content Updated!', 'success');
	},

	updateModule: async () => {
		await patchModule.run();
		await this.getModules();
		showAlert('Module Updated', 'success');
		closeModal('mdl_addModule');
	},

	addModule: async () => {
		await createModule.run();
		await this.getModules();
		showAlert('Module Created', 'success');
		closeModal('mdl_addModule');
	},

	addUser: async () => {
		try {

			showAlert(`User ${MultiSel_Allergies.selectedOptions.map(item => item.value)}`, "info");
			//showAlert(`User ${MultiSel_Allergies.options}`, " Add")

			const response = await fetch('http://10.10.16.31:8000/user_profile', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({
					username: inp_userName.text, 
					gender: sel_Gender.selectedOptionValue,
					age: inp_Age.text,
					allergies: MultiSel_Allergies.selectedOptions.map(item => item.value),
					//preferredCategories: MultiSel_Preferred.selectedOptions.map(item => item.value),
					//notificationPreferences: MultiSel_NonPreffered.selectedOptions.map(item => item.value),
					//desc: inp_userDesc.text,

				})
			});
			if (!response.ok) throw new Error('Failed to add user');
			await this.getModules();
			showAlert('User Created', 'success');
			closeModal('mdl_addUser');
		} 
		catch (e) {
			showAlert(e.message, 'error');
		}
	}	

}