let likes = document.querySelectorAll('.like');
let spans = document.querySelectorAll('.counter');
for (let i = 0; i < likes.length; ++i) {
    spans[i].innerHTML = likes[i].getAttribute('data-count')
}

$(".plus").on('click', function () {
      const request = new Request(
          'http://127.0.0.1:8000/like/',
          {
              method: 'POST',
              headers: {
                  'X-CSRFToken': csrftoken,
                  'content-type': 'application/json'
              },
              body: JSON.stringify({
                    question_id: $(this).parent(".like").data('id'),
                    type: 'like'
                  }
              )
          }
      )

      fetch(request).then(
          response_raw => response_raw.json().then(
                response_json => {
                    if (response_json.status === "ok") {
                        $(this).parent(".like").attr("data-count", response_json.likes_count)
                        let likes = document.querySelectorAll('.like');
                        let spans = document.querySelectorAll('.counter');
                        for (let i = 0; i < likes.length; ++i) {
                            spans[i].innerHTML = likes[i].getAttribute('data-count')
                        }
                    } else {
                        alert(response_json.message)
                    }
                }
          )
      );
})


$(".minus").on('click', function () {
      const request = new Request(
          'http://127.0.0.1:8000/like/',
          {
              method: 'POST',
              headers: {
                  'X-CSRFToken': csrftoken,
                  'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                  question_id: $(this).parent(".like").data('id'),
                  type: 'dislike'
              }),
          }
      )

      fetch(request).then(
          response_raw => response_raw.json().then(
                response_json => {
                    if (response_json.status === "ok") {
                        $(this).parent(".like").attr("data-count", response_json.likes_count)
                        let likes = document.querySelectorAll('.like');
                        let spans = document.querySelectorAll('.counter');
                        for (let i = 0; i < likes.length; ++i) {
                            spans[i].innerHTML = likes[i].getAttribute('data-count')
                        }
                    } else {
                        alert(response_json.message)
                    }
                }
          )
      );
})
