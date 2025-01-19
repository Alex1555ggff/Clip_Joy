function reactions(video_name, status) {
		let form_data = new FormData()

		form_data.append('video_name', video_name)
        form_data.append('status', status)
		form_data.append(
			'csrfmiddlewaretoken',
			document.querySelector('input[name=csrfmiddlewaretoken]').value
		)

		fetch('/like', {
			method: 'POST',
			body: form_data,
		}).then(response => {
			if (response.ok) {
				if (response.status === 200) {
					let reactions_count = parseInt(
						document.getElementById(status + "_count").innerText) + 1
					document.getElementById(status + "_count").innerText = reactions_count
                    document.getElementById(status).className = status + ' active'
					console.log('200 Ok')
					
				} else if (response.status === 202) {
					let reactions_count = parseInt(
						document.getElementById(status + "_count").innerText) - 1
					document.getElementById(status + "_count").innerText = reactions_count
                    document.getElementById(status).className = status
					console.log('202 Ok')

				} else if (response.status === 201) {
                    if (status == 'like') { var old_status = 'dislike'}
                    else if (status == 'dislike') { var old_status = 'like'}
                    console.log(old_status)
                
					let reactions_count = parseInt(
						document.getElementById(status + "_count").innerText) + 1
					document.getElementById(status + "_count").innerText = reactions_count
                    document.getElementById(status).className = status + ' active'

                    let reactions_count2 = parseInt(
						document.getElementById(old_status + "_count").innerText) - 1
					document.getElementById(old_status + "_count").innerText = reactions_count2
                    document.getElementById(old_status).className = old_status

					console.log('201 Ok')
				}
			} else if (response.status === 401) {
					alert("Войдите в аккаунт чтобы оценивать видео")
					console.log('401 Unauthorized')
				}
		})
}