function submitImage() {
  // action for the submit button
  console.log("submit");
	location.replace("{{ url_for('template',filename='index.html') }}")
  }

