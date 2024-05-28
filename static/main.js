
        function toggleTheme() {
            const body = document.body;
            body.classList.toggle('dark !important');


        }

        function toggleRightAside() {
          const aside = document.querySelector('.aside2');
          aside.classList.toggle('hidden');
      }

      function toggleLeftAside() {
          const aside = document.querySelector('.aside1');
          aside.classList.toggle('drawer-open');
      }
            function toggleRightAside() {
              const aside = document.querySelector('.aside2');
              aside.classList.toggle('hidden');
            }


            document.getElementById('dropdownBtn').addEventListener('click', function() {
              var menu = document.getElementById('dropdownMenu');
              menu.classList.toggle('hidden');
            });
  
            

//Q&A



  function likeAnswer(answerId) {
    var likeButton = document.getElementById("likeButton" + answerId);
    var likeCount = document.getElementById("likeCount" + answerId);
    var csrfToken = document.querySelector("input[name='csrfmiddlewaretoken']").value;

    fetch("/like-answer/", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": csrfToken,
      },
      body: JSON.stringify({
        answer_id: answerId,
      }),
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.liked) {
          likeButton.innerHTML =
            '<svg class="w-4 h-4 fill-current mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/><path fill-rule="evenodd" d="M10 0a10 10 0 100 20 10 10 0 000-20zm0 18a8 8 0 100-16 8 8 0 000 16zm0-14a1 1 0 011 1v5a1 1 0 11-2 0V5a1 1 0 011-1z" clip-rule="evenodd"/></svg>';
        } else {
          likeButton.innerHTML =
            '<svg class="w-4 h-4 fill-current mr-1" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20"><path d="M10 12a2 2 0 100-4 2 2 0 000 4z"/><path fill-rule="evenodd" d="M10 0a10 10 0 100 20 10 10 0 000-20zm0 18a8 8 0 100-16 8 8 0 000 16zm0-14a1 1 0 011 1v5a1 1 0 11-2 0V5a1 1 0 011-1z" clip-rule="evenodd"/></svg>';
        }
        likeCount.textContent = data.like_count;
      })
      .catch((error) => console.error("Error:", error));
  }

  function toggleReplies(answerId) {
    var repliesDiv = document.getElementById("replies-" + answerId);
    if (repliesDiv.style.display === "none" || !repliesDiv.style.display) {
      repliesDiv.style.display = "block";
    } else {
      repliesDiv.style.display = "none";
    }
  }

