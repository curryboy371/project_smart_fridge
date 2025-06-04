export default {
	recipe: "None",


	async click_recipe() {
		const response = await GET_GPTTEST.run();
		this.recipe = response.response;
	},


}