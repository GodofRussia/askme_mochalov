$(".check-correct").on('click', function (e) {
      const request = new Request(
          'http://127.0.0.1:8000/make_correct/',
          {
              method: 'POST',
              headers: {
                  'X-CSRFToken': csrftoken,
                  'content-type': 'application/json'
              },
              body: JSON.stringify({
                    answer_id: $(this).data('id'),
                    question_id: $(this).data('question-id'),
                    status: this.checked
                  }
              )
          }
      )

      fetch(request).then(
          response_raw => response_raw.json().then(
                response_json => {
                    if (response_json.status === "ok") {
                        $(this).attr("data-status", response_json.answer_status)
                        this.checked = response_json.answer_status
                    } else {
                        this.checked = false
                        alert(response_json.message);
                    }
                }
          )
      );
})