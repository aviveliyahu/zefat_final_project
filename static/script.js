// identify if user is registered in our DB
function log(event) {
	event.preventDefault();
	const date = new Date();
	const hour = date.getHours();
	const minute = date.getMinutes();
	const second = date.getSeconds();
	const str_time = hour + ":" + minute + ":" + second;
	let id = parseInt(document.forms["id_form"]["id"].value);
	let form = document.forms['id_form'];
    let formData = new FormData(form);
    let selectedLLM = formData.get('llm');
	fetch('/llm', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ user_id :id,msg: selectedLLM })
	}).then(response => response.json()
	).then(function (data) {
		let path = data.response;
		if (path==="0"){
			console.log("User tried to log at " + str_time + " but failed, ID entered was: " + id);
			alert("ID not found in the database, please try again.");
			document.getElementById("input1").value = '';
		}
		else{
			window.location.href = path;
		}
	})
};


// update chat box
document.getElementById('messageArea').addEventListener('submit', function (event) {
	const date = new Date();
	const hour = date.getHours();
	const minute = date.getMinutes();
	const str_time = hour + ":" + minute;

	let rawText = document.getElementById("text").value;

	let userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + rawText + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="static/img/user.png" class="rounded-circle user_img_msg"></div></div>';

	document.getElementById("text").value = "";
	document.getElementById("messageFormeight").insertAdjacentHTML('beforeend', userHtml);

	let loading = '<div id="loading" class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="static/img/open-ai.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">'+'<img src="static/img/loading.gif" width="20" height="20"></img>' +'</div></div>';
	document.getElementById("messageFormeight").insertAdjacentHTML('beforeend', loading);

	fetch('/get', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ msg: rawText })
	}).then(response => response.json()
	).then(function (data) {
		let msg = data.response;
		let botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="static/img/open-ai.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + msg + '<span class="msg_time">' + str_time + '</span></div></div>';
		document.getElementById("loading").remove();
		document.getElementById("messageFormeight").insertAdjacentHTML('beforeend', botHtml);


		let chatBox = document.getElementById('messageFormeight');
		chatBox.scrollTop = chatBox.scrollHeight; // auto scroll to the bottom
		if (data === "Chat saved!") {
			let inputBox = document.getElementById('text');
			inputBox.disabled = true;
			inputBox.placeholder = "Chat ended.";
			document.getElementById("send1").disabled = true;
			document.getElementById("send1").type = "button";

			document.getElementById("save1").disabled = true;
			document.getElementById("save1").type = "button";
		}
	});
	event.preventDefault();
});


// save chat
document.getElementById("save1").addEventListener("click", function () {
	const date = new Date();
	const hour = date.getHours();
	const minute = date.getMinutes();
	const str_time = hour + ":" + minute;
	let rawText = "Save chat.";

	let userHtml = '<div class="d-flex justify-content-end mb-4"><div class="msg_cotainer_send">' + "Save chat." + '<span class="msg_time_send">' + str_time + '</span></div><div class="img_cont_msg"><img src="static/img/user.png" class="rounded-circle user_img_msg"></div></div>';

	document.getElementById("text").value = "";
	document.getElementById("messageFormeight").insertAdjacentHTML('beforeend', userHtml);


	fetch('/get', {
		method: 'POST',
		headers: {
			'Content-Type': 'application/json'
		},
		body: JSON.stringify({ msg: rawText })
	}).then(response => response.json()
	).then(function (data) {
		let msg = data.response;
		let botHtml = '<div class="d-flex justify-content-start mb-4"><div class="img_cont_msg"><img src="static/img/open-ai.png" class="rounded-circle user_img_msg"></div><div class="msg_cotainer">' + "Chat saved." + '<span class="msg_time">' + str_time + '</span></div></div>';
		document.getElementById("messageFormeight").insertAdjacentHTML('beforeend', botHtml);


		let chatBox = document.getElementById('messageFormeight');
		chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
		if (data.response === "Chat saved!") {
			let inputBox = document.getElementById('text');
			inputBox.disabled = true;
			inputBox.placeholder = "Chat ended.";
			document.getElementById("send1").disabled = true;
			document.getElementById("send1").type = "button";

			document.getElementById("save1").disabled = true;
			document.getElementById("save1").type = "button";
		}
	});
	event.preventDefault();
});


document.getElementById('logoutForm').addEventListener('submit', function(event) {
	event.preventDefault();  
	fetch(this.action, { method: 'POST' })
		.then(() => {
			window.location.href = '/';
		});
});