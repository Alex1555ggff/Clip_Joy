function subscribe(channel_name) {
	let run = confirm('Подписаться на '+ channel_name + '?')
	if (run){
		let form_data = new FormData()

		form_data.append('channel_name', channel_name)
		form_data.append(
			'csrfmiddlewaretoken',
			document.querySelector('input[name=csrfmiddlewaretoken]').value
		)

		fetch('/subscribe', {
			method: 'POST',
			body: form_data,
		}).then(response => {
			if (response.ok) {
				if (response.status === 200) {
					let subscribers_count = parseInt(
						document.getElementById("subscribers-count").innerText) + 1
					document.getElementById("subscribers-count").innerText = subscribers_count
					document.getElementById("subscribe-btn-id").className = "subscribe-btn active"
					console.log('200 Ok')
					
				} else if (response.status === 201) {
					let subscribers_count = parseInt(
						document.getElementById("subscribers-count").innerText) - 1
					document.getElementById("subscribers-count").innerText = subscribers_count
					document.getElementById("subscribe-btn-id").className = "subscribe-btn"
					console.log('201 Ok')
				
				}
			} else if (response.status === 401) {
					alert('Войдите в аккаунт чтобы подписаться')
					console.log('401 Unauthorized')
				}
		})
}}

