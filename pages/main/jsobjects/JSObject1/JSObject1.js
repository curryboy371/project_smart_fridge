export default {

	async ping() {
		try {
			const response = await PING.run();
			showAlert(`Success: ${response.message}`); // 결과 보여주기
		} 
		catch (error) {
			showAlert(`에러: ${error}`);
		}
	}
}