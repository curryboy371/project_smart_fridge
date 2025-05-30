export default {
	moduleContent: {},
	addQuestion: false,
	showNewQuestion: false,
	newQuestionType: '',
	newQuizQuestions: [],
	
	setNewQuestionType: (type) => {
		this.newQuestionType = type;
	},

	setNewQuizQuestions: (quizQuestions) => {
		this.newQuizQuestions = quizQuestions;
	},

	setAddQuestion: (isAddQuestion) => {
		this.addQuestion = isAddQuestion;
	},

	setShowNewQuestion: (isShowNewQuestion) => {
		this.showNewQuestion = isShowNewQuestion;
	},

	setModuleContent: async (moduleContent) => {
		const quiz = await fetchQuizContent.run({
			id: moduleContent.id
		});
		const contentType = moduleContent.content_type;
		let content;

		if (contentType === 'Reading Material') {
			content = await fetchReadingContent.run({id: moduleContent.id});
		}
		if (contentType === 'Video') {
			console.log(moduleContent)
			content = await fetchVideoContent.run({id: moduleContent.id});
		}
		if (contentType === 'Quiz') {
			const quizQuestions = await fetchQuizQuestions.run({quizId: quiz[0].id});
			content = [{
				...quiz[0],
				questions: quizQuestions
			}]
		}

		this.moduleContent = {
			moduleContent,
			content: content.length > 0 ? content[0] : undefined,
		}
	},

	updateVideoContent: async () => {
		await patchVideoContent.run();
		closeModal('mdl_manageContent');
		showAlert('Content Updated!', 'success')
	},

	updateReadingContent: async () => {
		await patchReadingContent.run()
		closeModal('mdl_manageContent');
		showAlert('Content Updated!', 'success')
	},

	deleteContent: async () => {
		if (this.moduleContent.moduleContent.content_type === 'Video') {
			await deleteVideoContent.run();
		}
		closeModal('mdl_manageContent');
		showAlert('Content Deleted!', 'success')
	},

	updateQuiz: async () => {
		const quiz = lst_updateQuiz.selectedItem;
		let quizQuestion;
		if (quiz.type === 'Single Answer') {
			quizQuestion = {
				id: quiz.id,
				answer: inp_updateSingleAnswer.text,
				answerOptions: null
			}
		};
		if (quiz.type === 'True or False') {
			quizQuestion = {
				id: quiz.id,
				answer: rad_updateBooleanAnswer.selectedOptionValue,
				answerOptions: null
			}
		}
		if (quiz.type === 'Multiple choice') {

			let answer = '';

			if (chk_updateMultiChoiceAnswerA.isChecked) {
				if (answer.length > 0) {
					answer += ","
				}
				answer += inp_updateMultiChoiceA.text
			}

			if (chk_updateMultiChoiceAnswerB.isChecked) {
				if (answer.length > 0) {
					answer += ","
				}
				answer += inp_updateMultiChoiceB.text
			}

			if (chk_updateMultiChoiceAnswerC.isChecked) {
				if (answer.length > 0) {
					answer += ","
				}
				answer += inp_updateMultiChoiceC.text
			}

			if (chk_updateMultiChoiceAnswerD.isChecked) {
				if (answer.length > 0) {
					answer += ","
				}
				answer += inp_updateMultiChoiceD.text
			}

			quizQuestion = {
				id: quiz.id,
				answer,
				answerOptions: inp_updateMultiChoiceA.text + ',' + inp_updateMultiChoiceB.text + ',' + inp_updateMultiChoiceC.text + ',' + inp_updateMultiChoiceD.text, 
			}
		}

		await patchQuizContent.run();
		await patchQuizQuestion.run(quizQuestion);

		closeModal('mdl_manageContent');
		showAlert('Quiz Content Updated!', 'success')
	},

	createQuizQuestion: async () => {
		let answerOptions = '';
		let answer = '';
		if (sel_addQuizQuestionType.selectedOptionValue === 'Multiple choice') {
			answerOptions = inp_updateMultiChoiceA.text + ',' + inp_updateMultiChoiceB.text + ',' + inp_updateMultiChoiceC.text + ',' + inp_updateMultiChoiceD.text;
		}
		if (sel_addQuizQuestionType.selectedOptionValue === 'Single Answer') {
			answerOptions = inp_updateSingleAnswer.text;
		}
		if (sel_addQuizQuestionType.selectedOptionValue === 'True or False') {
			answerOptions = 'True, False'
		}
		if (sel_addQuizQuestionType.selectedOptionValue === 'Single Answer') {
			answer = inp_updateSingleAnswer.text;
		};
		if (sel_addQuizQuestionType.selectedOptionValue === 'True or False') {
			answer = rad_updateBooleanAnswer.selectedOptionValue;
		}
		if (sel_addQuizQuestionType.selectedOptionValue === 'Multiple choice') {

			let singleAnswer = '';

			if (chk_updateMultiChoiceAnswerA.isChecked) {
				if (singleAnswer.length > 0) {
					singleAnswer += ","
				}
				singleAnswer += inp_updateMultiChoiceA.text
			}

			if (chk_updateMultiChoiceAnswerB.isChecked) {
				if (singleAnswer.length > 0) {
					singleAnswer += ","
				}
				singleAnswer += inp_updateMultiChoiceB.text
			}

			if (chk_updateMultiChoiceAnswerC.isChecked) {
				if (singleAnswer.length > 0) {
					singleAnswer += ","
				}
				singleAnswer += inp_updateMultiChoiceC.text
			}

			if (chk_updateMultiChoiceAnswerD.isChecked) {
				if (singleAnswer.length > 0) {
					singleAnswer += ","
				}
				singleAnswer += inp_updateMultiChoiceD.text
			}

			answer = singleAnswer;

		}
		const newQuestionArr = await createQuizQuestion.run({
			type: sel_addQuizQuestionType.selectedOptionValue,
			question: rte_updateQuizQuestion.text,
			quizContentId: this.moduleContent.content.id,
			answerOptions,
			answer,
		});

		if (newQuestionArr && newQuestionArr.length > 0) {
			this.setModuleContent({
				...this.moduleContent,
				content: {
					...this.moduleContent.content,
					questions: {
						...this.moduleContent.content.questions,
						...newQuestionArr[0]
					}
				}
			});
		}

		resetWidget('lst_updateQuiz');
		await this.setModuleContent(this.moduleContent.moduleContent);
		showAlert('Quiz Question Added!', 'success')
	},

	addNewQuestion: () => {
		const type = sel_newQuestionType.selectedOptionValue;
		let question = rte_newQuizQuestion.text;

		if (type === 'Single Answer') {
			this.newQuizQuestions = [
				...this.newQuizQuestions,
				{
					id: Math.random(),
					question,
					answer: inp_newSingleAnswer.text,
					answerOptions: null,
				}
			]
		}
		if (type === 'True or False') {
			this.newQuizQuestions = [
				...this.newQuizQuestions,
				{
					id: Math.random(),
					question,
					answer: rad_newTrueOrFalse.selectedOptionValue,
					answerOptions: null,
				}
			]
		}
		if (type === 'Multiple choice') {
			let singleAnswer = '';

			if (chk_newMultiChoiceAnswerA.isChecked) {
				if (singleAnswer.length > 0) {
					singleAnswer += ","
				}
				singleAnswer += inp_newMultiChoiceA.text
			}

			if (chk_newMultiChoiceAnswerB.isChecked) {
				if (singleAnswer.length > 0) {
					singleAnswer += ","
				}
				singleAnswer += inp_newMultiChoiceB.text
			}

			if (chk_newMultiChoiceAnswerC.isChecked) {
				if (singleAnswer.length > 0) {
					singleAnswer += ","
				}
				singleAnswer += inp_newMultiChoiceC.text
			}

			if (chk_newMultiChoiceAnswerD.isChecked) {
				if (singleAnswer.length > 0) {
					singleAnswer += ","
				}
				singleAnswer += inp_newMultiChoiceD.text
			}

			this.newQuizQuestions = [
				...this.newQuizQuestions,
				{
					id: Math.random(),
					question,
					answer: singleAnswer,
					answerOptions: inp_newMultiChoiceA.text + ',' + inp_newMultiChoiceB.text + ',' + inp_newMultiChoiceC.text + ',' + inp_newMultiChoiceD.text,
				}
			]
		}

		resetWidget('rte_newQuizQuestion');
		resetWidget('sel_addQuizQuestionType');
	},

	removeQuizContent: async () => {
		await deleteQuizContent.run();

		closeModal('mdl_manageContent');
	},

	createReadingMaterial: async () => {
		const courseContentArr =  await createModuleContent.run({
			title: inp_newReadingTitle.text
		});

		if (courseContentArr && courseContentArr.length > 0) {
			await createReadingContent.run({
				courseContentId: courseContentArr[0].id
			})
		}

		closeModal('mdl_addContent');
		showAlert('Content Created!', 'success');
	},

	createVideoMaterial: async () => {
		const courseContentArr =  await createModuleContent.run({
			title: inp_newVideoTitle.text
		});

		if (courseContentArr && courseContentArr.length > 0) {
			await createVideoContent.run({
				courseContentId: courseContentArr[0].id
			})
		}

		closeModal('mdl_addContent');
		showAlert('Content Created!', 'success');
	},

	createQuizMaterial: async () => {
		const courseContentArr =  await createModuleContent.run({
			title: inp_newQuizTitle.text
		});

		if (courseContentArr && courseContentArr.length > 0) {
			if (utils.newQuizQuestions.length > 0) {
				const quizContent = await createQuizContent.run({
					courseModuleContentId: courseContentArr[0].id
				})
				console.log('quizContent', quizContent);
				if (quizContent && quizContent.length > 0) {
					utils.newQuizQuestions.map(async q => {
						await createQuizQuestion.run({
							type: sel_newQuestionType.selectedOptionValue,
							question: q.question,
							quizContentId: quizContent[0].id,
							answerOptions: q.answerOptions,
							answer: q.answer,
						})
					});
				}
			}
		}

		closeModal('mdl_addContent');
		showAlert('Content Created!', 'success');
	},
}