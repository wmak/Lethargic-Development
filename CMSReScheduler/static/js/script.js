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