export default {

	state: {
		server_time: "None"
	},



	async ping() {
		try {

			await this.get_servertime();
			const response = await PING.run();
			showAlert(`Success: ${response.message}`); // 결과 보여주기


		} 
		catch (error) {
			showAlert(`에러: ${error}`);
		}
	},

	async get_servertime() {
		try {
			const response = await GET_time.run();
			this.state.server_time =response.time; 
		} 
		catch (error) {
			showAlert(`에러: ${error}`);
		}
	},
}