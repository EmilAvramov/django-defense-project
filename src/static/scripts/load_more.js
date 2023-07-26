document.addEventListener('DOMContentLoaded', function () {
	var loadMoreBtn = document.getElementById('load_more__btn');
	var searchResults = document.querySelector('.search__results');

	if (loadMoreBtn) {
		loadMoreBtn.addEventListener('click', function () {
			fetchNextPage();
		});
	}

	function fetchNextPage() {
		var nextPageUrl = loadMoreBtn ? loadMoreBtn.dataset.url : null;
		var cleanUrl = nextPageUrl.replace(/&amp;/g, '&');
		fetch(`/search/?nextPage=${encodeURIComponent(cleanUrl)}`, {
			method: 'GET',
			headers: {
				'X-CSRFToken': csrfToken,
			},
		})
			.then(function (response) {
				return response.json();
			})
			.then(function (data) {
				console.log(data);
				if (data && !data.error) {
					var items = data.content;
					var fragment = document.createDocumentFragment();

					items.forEach(function (item) {
						var resultItem = document.createElement('div');
						resultItem.innerHTML = `<div class="search__result_card" data-pos="${item.id}">
												   <a href="{% url 'main_app:search' ${item.id} %}">
													 <div class="card__name">${item.name}</div>
													 <img class="card__image" src="${item.image}" alt="digimon image"/>
												   </a>
												 </div>`;
						fragment.appendChild(resultItem);
					});

					searchResults.innerHTML = '';
					searchResults.appendChild(fragment);

					loadMoreBtn.dataset.url = data.pageable.nextPage;

					if (!data.pageable.nextPage) {
						loadMoreBtn.style.display = 'none';
					}
				} else {
					console.error('Error fetching next page.');
				}
			})
			.catch(function (error) {
				console.error('Error fetching next page.', error);
			});
	}
});
