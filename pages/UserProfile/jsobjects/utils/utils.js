export default {
	// 상태 객체
	state: {
		modalMode: 'add',      // 'add' 또는 'edit'
		currentData: null,     // 편집 시 해당 데이터 저장
		isModalOpen: false,    // 모달 열림 상태

		defaultAllergies: [],
		defaultpreferredCategories: [],
		defaultmissingNutrients: []
	},

	categoryTable: {
		allergies: [],
		nutrition: [],
		storage_method: [],
		food_simple: [],
	},

	loadCategoryTable: async () => {

		const nutrition_data = await GET_nutrition.run();
		this.categoryTable.nutrition = nutrition_data.map(item => ({
			label: item.name,
			value: item.value
		}));

		const allergies_data = await GET_allergies.run();
		this.categoryTable.allergies = allergies_data.map(item => ({
			label: item.name,
			value: item.value
		}));

		const storage_data = await GET_storage_method.run();
		this.categoryTable.storage_method = storage_data.map(item => ({
			label: item.name,
			value: item.value
		}));

		const food_simple_data = await GET_food_simple_category.run();
		this.categoryTable.food_simple = food_simple_data.map(item => ({
			label: item.name,
			value: item.value
		}));
	},



	// 사용자 추가 모드로 모델 열기
	openAddModal() {
		this.state.modalMode = 'add';
		this.state.currentData = null;
		this.state.isModalOpen = true;

		this.state.defaultAllergies = [];
		this.state.defaultpreferredCategories = [];
		this.state.defaultmissingNutrients = [];
	},

	// 사용자 편집 모드로 모달 열기 (id 또는 user data 받아서 처리)
	openEditModal(userdata) {
		this.state.modalMode = 'edit';
		this.state.currentData = userdata;
		this.state.isModalOpen = true;

		const toLabelValue = arr => 
		Array.isArray(arr) 
		? arr.map(code => ({ label: code, value: code })) 
		: [];

		this.state.defaultAllergies = toLabelValue(userdata.allergies);
		this.state.defaultpreferredCategories = toLabelValue(userdata.preferredCategories);
		this.state.defaultmissingNutrients = toLabelValue(userdata.missingNutrients);

	},

	// state 리셋
	resetStateData: () => {
		this.state.modalMode = '';
		this.state.currentData = null;
		this.state.isModalOpen = false;

		this.state.defaultAllergies = [];
		this.state.defaultpreferredCategories = [];
		this.state.defaultmissingNutrients = [];
	},

	// 사용자 목록 로드
	loadUser: async () => {
		await GET.run();
	},

	editUser: async () => {
		// 널 체크
		if (!utils.state.currentData) {
			showAlert("수정할 사용자 정보가 없습니다.", "warning");
			console.log("currentData is null or undefined");
			return;
		}



		try {
			// 바디 미리 준비
			const allergies = Array.isArray(MultiSel_Allergies.selectedOptions) ? MultiSel_Allergies.selectedOptions.map(item => item.value) : [];
			const preferredCategories = Array.isArray(MultiSel_Preferred.selectedOptions) ? MultiSel_Preferred.selectedOptions.map(item => item.value) : [];
			const missingNutrients = Array.isArray(MultiSel_MissingNutrients.selectedOptions) ? MultiSel_MissingNutrients.selectedOptions.map(item => item.value) : [];

			const jsonres = {
				id: utils.state.currentData._id,
				username: inp_userName.text,
				gender: sel_Gender.selectedOptionValue,
				age: parseInt(inp_Age.text) || 0,
				allergies: allergies,
				preferredCategories: preferredCategories,
				missingNutrients: missingNutrients,
				desc: inp_userDesc?.text ?? ""
			};

			const response = await PUT.run({body: jsonres});
			showAlert("사용자 수정에 성공했습니다.", "success");
			console.log("응답 데이터:", response);
			await this.loadUser();
		} catch (e) {
			showAlert(e.message || "오류가 발생했습니다.", "error");
			console.log("Error detail:", e);
		}

	},

	addUser: async () => {
		try {

			const allergies = Array.isArray(MultiSel_Allergies.selectedOptions) ? MultiSel_Allergies.selectedOptions.map(item => item.value) : [];
			const preferredCategories = Array.isArray(MultiSel_Preferred.selectedOptions) ? MultiSel_Preferred.selectedOptions.map(item => item.value) : [];
			const missingNutrients = Array.isArray(MultiSel_MissingNutrients.selectedOptions) ? MultiSel_MissingNutrients.selectedOptions.map(item => item.value) : [];

			const jsonres = {
				username: inp_userName.text,
				gender: sel_Gender.selectedOptionValue,
				age: parseInt(inp_Age.text) || 0,
				allergies: allergies,
				preferredCategories: preferredCategories,
				missingNutrients: missingNutrients,
				desc: inp_userDesc?.text ?? ""
			};

			const response = await POST.run({body: jsonres});
			showAlert("사용자 등록에 성공했습니다.", "success");
			console.log("응답 데이터:", response);

			await this.loadUser();
		}
		catch(e) {
			showAlert(e.message || "오류가 발생했습니다.", "error");
			console.log("Error detail:", e);
		}
	},

	delete_user: async () => {

		const id = utils.state.currentData._id;
		try {
			console.log("try delete user :", id);
			const response = await DELETE.run( {id:id} );
			showAlert("사용자 제거에 성공했습니다.", "success");
			console.log("응답 데이터:", response);
			await this.loadUser();
		}
		catch(e) {
			showAlert(e.message || "오류가 발생했습니다.", "error");
			console.log("Error detail:", e);
		}
	},

}