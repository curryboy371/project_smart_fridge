export default {
	recipe: "None",


	async click_test() {
		const response = await GET_GPT_TEST.run();
		this.recipe = response.response;
	},

	async click_recipe() {
		
		const response = await POST_GPT.run();
		this.recipe = response.response;
	},


}