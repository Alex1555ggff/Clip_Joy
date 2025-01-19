function delvideo() {
	let run = confirm('Вы действительно хотите безвозвратно удалить видео')
	if (run){

		let form_data = new FormData()
        let video_name = prompt("Введите название видео, которого вы хотите удалить")

		form_data.append('video_name', video_name)
		form_data.append(
			'csrfmiddlewaretoken',
			document.querySelector('input[name=csrfmiddlewaretoken]').value
		)

		fetch('/delete_video', {
			method: 'POST',
			body: form_data,
		}).then(response => {
			if (response.ok) {
				if (response.status === 200) {
                    alert('Видео ' + video_name + ' успешно удалено')
					console.log('200 Ok')
				} 
				
			} else if (response.status === 404) {
					alert('Ошибка при удалении видео: ' + video_name + '.\nПроверьте было ли верно указано название видео и являетесь ли вы автором видео')
					console.log('404 Error')
				}
		})
}}

