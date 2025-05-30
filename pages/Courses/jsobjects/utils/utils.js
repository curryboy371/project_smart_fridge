export default {

	updatedSubjectName: '',
	subject: {},

	setSubject: (subject) => {
		this.subject = subject; 
	},

	setUpdatedSubjectName: (name) => {
		this.updatedSubjectName = name; 
	},

	init: async () => {
		const courseTypes = await fetchCourseType.run();
		const courseLevels = await fetchCourseLevels.run();

		storeValue('types', courseTypes);
		storeValue('levels', courseLevels);
	},

	getSubjects: async () => {
		const subjects  = await fetchSubjects.run();
		const adjustedSubjects = subjects.map(s => {
			return {
				Id: s.id,
				Name: s.name,
			}
		});

		storeValue('subjects', adjustedSubjects);
	},



	createSubject: async () => 		{
		await createSubject.run({
			name: inp_subjectTitle.text
		});

		await this.getSubjects();
		closeModal('mdl_manageSubject');
		showAlert('Subject Created!', 'success')
	},

	updateSubjectName: async () => {
		await patchSubjectName.run();

		await this.getSubjects();
		closeModal('mdl_manageSubject');
		showAlert('Subject Updated', 'success');
	},

	getCourseBySubject: async () => {
		const courses = await fetchCoursesBySubject.run();
		return courses.map(c => {
			return {
				Id: c.course_id,
				Name: c.course_name,
				Duration: c.course_duration,
				Description: c.course_description,
				Image: c.course_thumbnail_url,
				Type: c.type_name,
				Level: c.level_name,
				Instructor: c.course_instructor,
				Language: c.course_language,
			}
		})
	},

	updateCourse: async () => {

		let thumbnailUrl;

		if (fpk_uploadThumbnail.files.length > 0) {
			thumbnailUrl = await cloudinaryImageUpload.run({
				data: fpk_uploadThumbnail.files[0].data,
			});
		} else {
			thumbnailUrl = img_thumbnail.image;
		}

		await patchCourse.run({
			thumbnailUrl: thumbnailUrl.url
		});


		await this.getCourseBySubject();
		closeModal('mdl_handleCourse')
		showAlert('Course Updated!', 'success');
	},

	addCourse: async () => {

		let thumbnailUrl;

		if (fpk_uploadThumbnail.files.length > 0) {
			thumbnailUrl = await cloudinaryImageUpload.run({
				data: fpk_uploadThumbnail.files[0].data,
			});
		} else {
			thumbnailUrl = null;
		}

		await createCourse.run({
			thumbnailUrl: thumbnailUrl.url
		});


		await this.getCourseBySubject();
		closeModal('mdl_handleCourse')
		showAlert('Course Created!', 'success');
	},
}