function toggleNotifications(obj) {
	notifications = document.getElementById("notifications-box");
	if (notifications.style.display == 'block') {
		notifications.style.display = 'none';
		obj.className = obj.className.replace(" clicked", "");
	} else {
		notifications.style.display = 'block';
		obj.className.replace(" clicked", "");
		obj.className += " clicked";
    }
}

function selectUploadType(self, value) {
	if (self.options[self.selectedIndex].value == "schedule") {
		document.getElementById('department').style.display = "block";
		document.getElementById('instructor').style.display = "block";
		document.getElementById('file').style.display = "block";
		document.getElementById('submit').style.display = "block";
	} else if (self.options[self.selectedIndex].value == "course") {
		document.getElementById('department').style.display = "none";
		document.getElementById('instructor').style.display = "none";
		document.getElementById('file').style.display = "block";
		document.getElementById('submit').style.display = "block";
	} else if (self.options[self.selectedIndex].value == "enrolment"){
		document.getElementById('department').style.display = "none";
		document.getElementById('instructor').style.display = "none";
		document.getElementById('file').style.display = "block";
		document.getElementById('submit').style.display = "block";
	} else if (self.options[self.selectedIndex].value == "room"){
		document.getElementById('department').style.display = "none";
		document.getElementById('instructor').style.display = "none";
		document.getElementById('file').style.display = "block";
		document.getElementById('submit').style.display = "block";
	} else if (self.options[self.selectedIndex].value == "department_programs"){
		document.getElementById('department').style.display = "none";
		document.getElementById('instructor').style.display = "none";
		document.getElementById('file').style.display = "block";
		document.getElementById('submit').style.display = "block";
	} else if (self.options[self.selectedIndex].value == "students_programs"){
		document.getElementById('department').style.display = "none";
		document.getElementById('instructor').style.display = "none";
		document.getElementById('file').style.display = "block";
		document.getElementById('submit').style.display = "block";
	} else if (self.options[self.selectedIndex].value == "program_requirements"){
		document.getElementById('department').style.display = "none";
		document.getElementById('instructor').style.display = "none";
		document.getElementById('file').style.display = "block";
		document.getElementById('submit').style.display = "block";
	} else {
		document.getElementById('department').style.display = "none";
		document.getElementById('instructor').style.display = "none";
		document.getElementById('file').style.display = "none";
		document.getElementById('submit').style.display = "none";
	}
<<<<<<< HEAD
}
=======
}

$(document).ready(function() {
	$("body").on("click", "a.schedule-cell.course", function() {
		var url = "/course/" + $(this).find("#course").html();
		$.getJSON(url, function(data) {
			console.log(data);
		});
	});
});
>>>>>>> develop
