$(function () {
  let serviceIds = [];
  let uncheckedId;
  $('input[type="checkbox"]').change(function () {
    if ($(this).is(':checked')) {
      if ($(this).attr('data-type') === 'services') {
        serviceIds.push($(this).attr('data-id'));
      }
    } else {
      uncheckedId = $(this).attr('data-id');
      if ($(this).attr('data-type') === 'services') {
        serviceIds = serviceIds.filter((checked) => {
          return checked !== uncheckedId;
        });
      }
    }
  });

  $('#btn-register-hospital').click(function () {
    const selectedCity = $('select#city option:selected');
    const hospitalName = $('#hospital-name');
    const cardPrice = $('#card-price');
    const numberOfDoctors = $('#number-of-doctors');
    const lattitude = $('#lattitude');
    const longitude = $('#longitude');
    const imageUrl = $('#image-url');
    const description = $('#description');
    const numberOfDepartments = $('#number-of-departments');
    const numberOfAwards = $('#number-of-awards');
    const emailAddress = $('#email-address');
    const mapAddress = $('#map-address');
    const phoneNumber = $('#phone-number');
    const numberOfResearchLabs = $('#number-of-research-labs');

    const hospitalData = {
      name: hospitalName.val(),
      card_price: cardPrice.val(),
      number_of_doctors: numberOfDoctors.val(),
      lattitude: lattitude.val(),
      longitude: longitude.val(),
      image_url: imageUrl.val(),
      description: description.val(),
      number_of_awards: numberOfAwards.val(),
      number_of_departments: numberOfDepartments.val(),
      number_of_research_labs: numberOfResearchLabs.val(),
      email_address: emailAddress.val(),
      phone: phoneNumber.val(),
      location: mapAddress.val(),
    };

    $.ajax({
      url: 'http://localhost:5001/api/v1/cities',
      type: 'GET',
      contentType: 'application/json',
      success: function (response) {
        const cityToBeLinked = response.filter((city) => {
          return city.name === selectedCity.val();
        });
        if (cityToBeLinked) {
          const endpoint = `http://localhost:5001/api/v1/cities/${cityToBeLinked[0].id}/hospitals`;
          $.ajax({
            url: endpoint,
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(hospitalData),
            success: function (response) {
              const newHospitalId = response.id;
              if (newHospitalId) {
                const endpoint = `http://localhost:5001/api/v1/hospitals/${newHospitalId}/services`;
                $.ajax({
                  url: endpoint,
                  type: 'POST',
                  contentType: 'application/json',
                  data: JSON.stringify({
                    service_ids: serviceIds,
                  }),
                  success: function (response) {
                    location.reload(true);
                  },
                });
                return false;
              }
            },
          });
        }
      },
    });
    return false;
  });
});
