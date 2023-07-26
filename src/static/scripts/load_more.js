document.addEventListener('DOMContentLoaded', function () {
	var loadMoreBtn = document.getElementById('load_more__btn');
	var searchResults = document.querySelector('.search__results');

	if (loadMoreBtn) {
		loadMoreBtn.addEventListener('click', function () {
			fetchNextPage();
		});
	}

	function fetchNextPage() {
		var loadMoreBtn = document.getElementById('load_more__btn');
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
				if (data && !data.error) {
					var items = data.content;
					var fragment = document.createDocumentFragment();

                    items.forEach(function (item) {
                        var resultItem = document.createElement('div');
                        resultItem.innerHTML = `<div class="search__result_card" data-pos="${item.id}">
                                        <a href="/search/${item.id}/">
                                          <div class="card__name">${item.name}</div>
                                          <img class="card__image" src="${item.image}" alt="digimon image"/>
                                        </a>
                                      </div>`;
                        fragment.appendChild(resultItem);
                    });

					searchResults.innerHTML = '';
					searchResults.appendChild(fragment);

					if (data.pageable.nextPage) {
						var loadMoreBtn = document.createElement('button');
						loadMoreBtn.id = 'load_more__btn';
						loadMoreBtn.dataset.url = data.pageable.nextPage;
						loadMoreBtn.textContent = 'Load More';
						loadMoreBtn.addEventListener('click', function () {
							fetchNextPage();
						});
						searchResults.appendChild(loadMoreBtn);
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
