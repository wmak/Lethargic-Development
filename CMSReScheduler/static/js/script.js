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
		document.getElementById('instructor').style.display = "none";
		document.getElementById('file').style.display = "none";
		document.getElementById('submit').style.display = "none";
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

	$("body").on("change", "select[name='department']", function() {
		if ($(this).val() != "") {
			$("#instructor").css("display", "block");
			$("select[name='instructor'").html("<option value=''>Select Instructor</option>");
			var url = "/instructors/" + $(this).val();
			$.getJSON(url, function(data) {
				$.each(data.instructors, function(index) {
					$("select[name='instructor'").append("<option value='" + data.instructors[index] + "'>" + data.instructors[index] + "</option>");
				});
			});
		} else {
			$("#instructor").css("display", "none");
			$("#file").css("display", "none");
			$("#submit").css("display", "none");
			$("select[name='instructor'").html("<option value=''>Select Instructor</option>");
			$(this).closest("#schedule-view-form").attr("action", "/admin/schedule/");
		}
	});

	$("body").on("change", "select[name='instructor']", function() {
		if ($(this).val() != "") {
			$(this).closest("#schedule-view-form").attr("action", "/admin/schedule/" + $(this).val() + "/");
			$("#file").css("display", "block");
			$("#submit").css("display", "block");
		} else {
			$("#file").css("display", "none");
			$("#submit").css("display", "none");
			$(this).closest("#schedule-view-form").attr("action", "/admin/schedule/");
		}
	});

	$("#add-course-form").on("click", "#submit", function(e) {
		$.ajax({
			url: "/course/" + $("#add-course-form").find("input[name='code']").val() + "/",
			type: "POST",
			data: JSON.stringify({
				"code" : $("#add-course-form").find("input[name='code']").val(),
				"name" : $("#add-course-form").find("input[name='name']").val(),
				"enrolment" : $("#add-course-form").find("input[name='enrolment']").val(),
				"department" : $("#add-course-form").find("input[name='department']").val()
			}),
			dataType: 'json',
			success: function() {
				location.href = "/add_course?add=success"
			}, 
			error: function() {
				location.href = "/add_course?add=error"
			}
		});
		e.preventDefault();
	});

	$("#delete-course-form").on("click", "#submit", function(e) {
		var temp = $(this).closest("#delete-course-form").find("select[name='course'] option:selected").text().split(" - ");
		var course = temp[0];
		var section = temp[1];
		$.ajax({
			url: "/course/" + course + "/" + section + "/",
			type: "DELETE",
			success: function() {
				location.href = "/delete_course?delete=success"
			}, 
			error: function() {
				location.href = "/delete_course?delete=error"
			}
		});
		e.preventDefault();
	});

	$("#switch-course-form").on("click", "#submit", function(e) {
		var temp1 = $(this).closest("#switch-course-form").find("select[name='course1'] option:selected").text().split(" - ");
		var temp2 = $(this).closest("#switch-course-form").find("select[name='course2'] option:selected").text().split(" - ");
		var course1 = temp1[0];
		var course2 = temp2[0];
		var section1 = temp1[1];
		var section2 = temp2[1];
		$.ajax({
			url: "/course/" + course1 + "/" + section1,
			type: "PUT",
			data: JSON.stringify({
				"switch" : {
					"code" : course2,
					"section": section2
				}
			}),
			dataType: 'json',
			success: function() {
				location.href = "/switch_course?switch=success"
			}, 
			error: function() {
				location.href = "/switch_course?switch=error"
			}
		});
		e.preventDefault();
	});
});

