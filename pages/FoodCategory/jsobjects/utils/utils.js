export default {
	// 상태 객체
	state: {
		modalMode: 'add',      // 'add' 또는 'edit'
		currentData: null,     // 편집 시 해당 데이터 저장
		isModalOpen: false,    // 모달 열림 상태

		defaultAllergies: [],
		defaultNutrition: []
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
	openAddModal () {
		this.state.modalMode = 'add';
		this.state.currentData = null;
		this.state.isModalOpen = true;

		this.state.defaultAllergies = [];
		this.state.defaultNutrition = [];

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

		this.state.defaultAllergies = toLabelValue(userdata.allergenTags);
		this.state.defaultNutrition = toLabelValue(userdata.nutrition);
	},

	// state 리셋
	resetStateData: () => {
		this.state.modalMode = '';
		this.state.currentData = null;
		this.state.isModalOpen = false;

		this.state.defaultAllergies = [];
		this.state.defaultNutrition = [];
	},

	// 사용자 목록 로드
	loadUser: async () => {
		await GET.run();
	},

	editUser: async () => {
		try {
			const allergenTags = Array.isArray(MultiSel_Allergies.selectedOptions)
			? MultiSel_Allergies.selectedOptions.map(item => item.value)
			: [];

			const nutrition = Array.isArray(MultiSel_Nutrition.selectedOptions)
			? MultiSel_Nutrition.selectedOptions.map(item => item.value)
			: [];

			console.log("id", utils.state.currentData._id);

			const jsonres = {
				id: utils.state.currentData._id,
				name: inp_FoodName.text,
				food_category: sel_FoodCategory.selectedOptionValue,
				storageMethod: sel_StorageMethod.selectedOptionValue,
				shelfLifeDays: parseInt(inp_ShelfLife.text) || 0,
				allergenTags: allergenTags,
				nutrition: nutrition,
				desc: inp_CategoryDesc?.text ?? ""
			};

			console.log("jsonres",jsonres);

			const response = await PUT.run({ body: jsonres });  // PUT 또는 PATCH 사용
			showAlert("카테고리 수정에 성공했습니다.", "success");
			console.log("수정된 데이터:", response);

			await this.loadUser();  // 수정 후 리스트 갱신
			this.state.isModalOpen = false;  // 모달 닫기
		} catch (e) {
			showAlert(e.message || "수정 중 오류가 발생했습니다.", "error");
			console.log("Error detail:", e);
		}
	},


	addUser: async () => {
		try {
			const allergenTags = Array.isArray(MultiSel_Allergies.selectedOptions)
			? MultiSel_Allergies.selectedOptions.map(item => item.value)
			: [];

			const nutrition = Array.isArray(MultiSel_Nutrition.selectedOptions)
			? MultiSel_Nutrition.selectedOptions.map(item => item.value)
			: [];

			const jsonres = {
				name: inp_FoodName.text,
				food_category: sel_FoodCategory.selectedOptionValue,
				storageMethod: sel_StorageMethod.selectedOptionValue,
				shelfLifeDays: parseInt(inp_ShelfLife.text) || 0,
				allergenTags: allergenTags,
				nutrition: nutrition,
				desc: inp_CategoryDesc?.text ?? ""
			};

			const response = await POST.run({ body: jsonres });
			showAlert("카테고리 등록에 성공했습니다.", "success");
			console.log("응답 데이터:", response);

			await this.loadUser();
		} catch (e) {
			showAlert(e.message || "오류가 발생했습니다.", "error");
			console.log("Error detail:", e);
		}
	},

	delete_user: async () => {
		const id = utils.state.currentData._id;
		try {
			console.log("try delete food cateogory :", id);
			const response = await DELETE.run( {id:id} );
			showAlert("음식 제거에 성공했습니다.", "success");
			console.log("응답 데이터:", response);
			await this.loadUser();
		}
		catch(e) {
			showAlert(e.message || "오류가 발생했습니다.", "error");
			console.log("Error detail:", e);
		}
	},

}