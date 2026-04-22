---
layout: default
---

<!--CSS styles-->
<!-- <link rel="stylesheet" href="css/bootstrap.css">
<link rel="stylesheet" href="css/font-awesome.min.css">  
-->
<link rel="stylesheet" href="css/perfect-scrollbar-0.4.5.min.css">
<link rel="stylesheet" href="css/magnific-popup.css">
<link rel="stylesheet" href="css/style.css">
<link id="theme-style" rel="stylesheet" href="css/styles/default.css">


<!--/CSS styles-->
<!--Javascript files-->
<script type="text/javascript" src="js/jquery-1.10.2.js"></script>

<script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/bootstrap@4.6.2/dist/js/bootstrap.bundle.min.js"></script>

<script type="text/javascript" src="js/TweenMax.min.js"></script>
<script type="text/javascript" src="js/jquery.touchSwipe.min.js"></script>
<script type="text/javascript" src="js/jquery.carouFredSel-6.2.1-packed.js"></script>

<script type="text/javascript" src="js/modernizr.custom.63321.js"></script>
<script type="text/javascript" src="js/jquery.dropdownit.js"></script>

<script type="text/javascript" src="js/jquery.stellar.min.js"></script>
<script type="text/javascript" src="js/ScrollToPlugin.min.js"></script>

<!-- <script type="text/javascript" src="js/bootstrap.min.js"></script> -->

<script type="text/javascript" src="js/jquery.mixitup.min.js"></script>

<script type="text/javascript" src="js/masonry.min.js"></script>

<script type="text/javascript" src="js/perfect-scrollbar-0.4.5.with-mousewheel.min.js"></script>

<script type="text/javascript" src="js/magnific-popup.js"></script>
<script type="text/javascript" src="js/custom.js"></script>



            
<div class="pagecontents">

    
    <div class="section color-1" id="filters">
	<div class="section-container" style="padding: 0;">
	    <div class="row" style="margin-left: 0px; margin-right: 0px;">


                <div class="col-md-3 search-bar">
                        <div class="input-group">
                                <input type="text" class="search-input form-control" id="searchInput" placeholder="Search..." oninput="filterItems()">
                                <div class="input-group-append">
                                        <span class="input-group-text">
                                                <i class="fa fa-search"></i>
                                        </span>
                                </div>
                        </div>
                </div>


		<div class="col-md-6" style="padding: 0;">
  		<nav class="cd-navigation" style="height: 70px;">
    			<ul class="cd-nav">
      				<li class="cd-nav-item active" onclick="changeActive(0)"><a href="#">All</a></li>
      				<li class="cd-nav-item" onclick="changeActive(1)"><a href="#">Journals</a></li>
      				<li class="cd-nav-item" onclick="changeActive(2)"><a href="#">Conferences</a></li>
     				<li class="cd-nav-item" onclick="changeActive(3)"><a href="#">Editorials</a></li>
      				<li class="cd-nav-item" onclick="changeActive(4)"><a href="#">Books</a></li>
    			</ul>
  		</nav>
		</div>

		<div class="col-md-1" style="padding: 0;">
                <nav class="cd-navigation" style="height: 70px;">
                        <ul class="cd-nav">
                                <li class="cd-nav-item">
				<a href="get_bibtex.php" id="downloadLink" data-toggle="tooltip" data-placement="top" title="" data-original-title="Download selected BibTeX entries">
				<i class="fa fa-external-link"></i>
				</a>
				</li>
                        </ul>
                </nav>
                </div>

                <div class="col-md-2 year-selector">
                        <div class="input-group">
                        <select class="year-dropdown form-control" style="height: auto;" id="yearSelector" onchange="filterItems()">
                                <option value="">All Years</option>
                        </select>
                        </div>
                </div>


		<script>
		const yearSelector = document.getElementById('yearSelector');
	  	const currentYear = new Date().getFullYear();

	  	for (let year = 1994; year <= currentYear; year++) {
	 	   	const option = document.createElement('option');
    			option.value = year;
    			option.textContent = year;
    			yearSelector.appendChild(option);
 		}

                document.addEventListener("DOMContentLoaded", function() {
                        var downloadLink = document.getElementById("downloadLink");
                        var searchInput = document.getElementById("searchInput");

                        downloadLink.addEventListener("click", function(event) {
                                var value = searchInput.value.toLowerCase();
                                var selectedYear = yearSelector.value;
                                var newHref = downloadLink.getAttribute("href") + "?string=" + value + "&year=" + selectedYear;
                                downloadLink.setAttribute("href", newHref);
                        });
                });


		function filterItems() {
                        var input = document.getElementById("searchInput").value.toLowerCase();
                        var selectedYear = document.getElementById('yearSelector').value;
                        var activeNavItem = document.querySelector('.cd-nav-item.active');
                        var activeIndex = Array.from(activeNavItem.parentNode.children).indexOf(activeNavItem);
                        var paperTypes = ['0', 'jpaper', 'cpaper', 'vpaper', 'bpaper'];
                        var selectedType = paperTypes[activeIndex];

                        var items = document.getElementsByClassName("item");

                        for (var i = 0; i < items.length; i++) {
                                var title = items[i].querySelector(".pubtitle strong").textContent.toLowerCase();
                                var author = items[i].querySelector(".pubauthor").textContent.toLowerCase();
                                var itemYear = items[i].getAttribute('data-year');
                                var itemType = items[i].classList.contains(selectedType) || activeIndex === 0;

                                if (title.includes(input) || author.includes(input)) {
                                        if ((itemYear === selectedYear || selectedYear === '') && itemType) {
                                        	items[i].style.display = "block";
                                        } else {
                                                items[i].style.display = "none";
                                        }
                                } else {
                                        items[i].style.display = "none";
                                }
                        }
                }

                function changeActive(index) {
                        const navItems = document.querySelectorAll('.cd-nav-item');
                        navItems.forEach(item => {
                                item.classList.remove('active');
                        });
                        navItems[index].classList.add('active');
                        filterItems(); // call filterItems function after changing active item
                }


		</script>


	    </div>
	</div>
    </div>

    <div class="section color-1" id="pub-grid">
	<div class="section-container"  style="padding: 0;">

	    <div class="row">
		<div class="col-md-12">
		    <div class="pitems">

			<!-- ############ JOURNAL PAPER #################### -->
			{% include pubs_journal.php %} 

			<!-- ############ CONFERENCE PAPER #################### -->
			{% include pubs_conference.php %} 

			<!-- ############  Editorials  #################### -->
			{% include pubs_editorial.php %}
 
			<!-- ############  Books & Book Chapters #################### -->
			{% include pubs_book.php %} 

		    </div>
		</div>
	    </div>
	</div>
     </div>
</div>

