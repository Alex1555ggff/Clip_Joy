let comment_form = document.getElementById("comment_form")
comment_form.addEventListener('submit',
    function (e) {
        e.preventDefault()
        let comment_form_data = new FormData(this)
        fetch('/comment', {
            method: "POST",
            body: comment_form_data
        }).then(response => {
            if (response.ok) {
                if (response.status === 200) {
                let comments_set = document.getElementById("comments_set")
                let new_comment = document.createElement("li")
                let textarea = document.getElementById("id_text")
                let username = document.getElementById("username").value
                let user_logo = document.getElementById("userlogo").value
                let text = textarea.value
                new_comment.innerHTML =
                    `<div class="comment">
                        <div class="comment-author">
                            <img src="${user_logo}" alt="" />
                        </div>
                        <div class="comment-text">
                            <h4 style="margin-bottom: 5px">${username}</h4>
                            <p>${text}</p>
                        </div>
                    </div>`
                comments_set.append(new_comment)
                textarea.value = ""
                textarea.disabled = true
                textarea.placeholder = "Подождите. В целях безопасности частота отправки комментариев ограничена."

                let comment_count = document.getElementById("comment_count").innerText
                document.getElementById("comment_count").innerText = +comment_count + 1
                
                setTimeout(function () {
                    let textarea = document.getElementById("id_text")
                    textarea.disabled = false
                    textarea.placeholder = "Введите свой комментарий"
                }, 5000)}
            } else if (response.status === 401) {
                    alert('Войдите в аккаунт чтобы оставлять комментарии')
                    console.log('401 Unauthorized')
                }
        })
    }
)