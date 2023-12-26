console.log('theme clicked!')

let theme = localStorage.getItem('theme')

if(theme === null){
	theme = 'blue';
	setTheme(theme);
}else{
	setTheme(theme)
}

let themeDots = document.getElementsByClassName('theme-dot')


for (var i=0; themeDots.length > i; i++){
	themeDots[i].addEventListener('click', function(){
		let mode = this.dataset.mode
		console.log('Option clicked:', mode)
		setTheme(mode)
	})
}

function setTheme(mode){
	if(mode == 'light'){
		document.getElementById('theme-style').href = defaultCSS;
	}

	if(mode == 'blue'){
		document.getElementById('theme-style').href = blueCSS;
	}

	if(mode == 'green'){
		document.getElementById('theme-style').href = greenCSS;
	}

	if(mode == 'purple'){
		document.getElementById('theme-style').href = purpleCSS;
	}

	localStorage.setItem('theme', mode)
}

//Toggle themes container
document.querySelector('.themes-toggle-icon').addEventListener('click',() => {
    document.querySelector('.themes-container').classList.toggle('hidden');
  });
