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

}

$(document).ready(function() {
	$("body").on("click", "a.schedule-cell.course", function() {
		var url = "/course/" + $(this).find("#course").html();
		$.getJSON(url, function(data) {
			console.log(data);
		});
	});

	$("#schedule-view-form").on("change", "select[name='department']", function() {
		if ($(this).val() != "") {
			$("#instructor").css("display", "block");
			$("select[name='instructor'").html("<option value=''>Select Instructor</option>");
			$(this).closest("#schedule-view-form").attr("action", "/schedule/" + $(this).val() + "/");
			var url = "/instructors/" + $(this).val();
			$.getJSON(url, function(data) {
				$.each(data.instructors, function(index) {
					$("select[name='instructor'").append("<option value='" + data.instructors[index] + "'>" + data.instructors[index] + "</option>");
				});
			});
		} else {
			$("#instructor").css("display", "none");
			$("#submit").css("display", "none");
			$("select[name='instructor'").html("<option value=''>Select Instructor</option>");
			$(this).closest("#schedule-view-form").attr("action", "/schedule/");
		}
	});

	$("#schedule-view-form").on("change", "select[name='instructor']", function() {
		action = $(this).closest("#schedule-view-form").attr("action");
		if ($(this).val() != "") {
			if ((action.split("/").length - 1) == 4) {
				$(this).closest("#schedule-view-form").attr("action", action.substring(0, action.lastIndexOf("/", action.length - 2)) + "/" + $(this).val() + "/")
			} else {
				$(this).closest("#schedule-view-form").attr("action", action + $(this).val() + "/");
			}
			$("#submit").css("display", "block");
		} else {
			$("#submit").css("display", "none");
			$(this).closest("#schedule-view-form").attr("action", action.substring(0, action.lastIndexOf("/", action.length - 2)) + "/");
		}
	});
});

