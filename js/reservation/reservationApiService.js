function appData() {
    const baseUrl = window.location.origin;


    return {
        name: "",
        doctors: [],
        selectedDoctorId: '',
        selectedDoctor: {},
        showCalendar: false,
        shiftsDays: [],

        setName: function (name) {
            this.name = name;
        },

        init() {
            fetch(`${baseUrl}/api/test.json`)
                .then((response) => response.json())
                .then((json) => this.doctors = json);
        },

        filterDoctor() {
            if (this.selectedDoctorId) {
                // var swiperTermsCalendar = new Swiper('.js-terms-calendar', {
                //     //watchOverflow: true,
                //     // spaceBetween: 0,
                //     // centeredSlides: true,
                //     // loop: true,
                //     slidesPerView: 2,
                //     // slidesPerGroup: 2,  
                //     navigation: {
                //         prevEl: '.js-terms-calendar--prev',
                //         nextEl: '.js-terms-calendar--next',
                //     },
                //     breakpoints: {
                //         551: {
                //         slidesPerView: 3,
                //         slidesPerGroup: 4,
                //         // spaceBetween: 60,
                //         },
                //         850: {
                //         slidesPerView: 4,
                //         slidesPerGroup: 4,
                //         //spaceBetween: 30,
                //         },
                //         1024: {
                //         slidesPerView: 4,
                //         slidesPerGroup: 4,
                //         //spaceBetween: 30,
                //         },
                //         1201: {
                //         slidesPerView: 4,
                //         slidesPerGroup: 4,
                //             //spaceBetween: 30,
                //         },
                //     }             
                // });
                this.showCalendar = true;
                console.log('filterDoctor');
                this.selectedDoctor = this.doctors.find(doctor => {
                    return doctor.id == this.selectedDoctorId;
                });

                this.shiftsDays = this.selectedDoctor.doctorshifts.map((day) => {
                    const startValue = day.shiftStartTime.split(":")[0].replace(/^0+/, '');
                    const endValue = day.shiftEndTime.split(":")[0].replace(/^0+/, '');

                    
                    const hours = [];
                    console.log(startValue);

                    for (let i = startValue; i <= endValue; i++) {
                        let prefix = ''
                        if (i < 10) {
                            prefix = '0';
                        } 

                        const singleDateTime = new Date(`${day.date}T${prefix}${i}:00:00`);
                        // const singleDateTime = new Date(`${day.date}T12:00:00`);
                        console.log('i:', i);

                        const hourObject = {
                            singleDateTime: singleDateTime.toLocaleString(),
                            status: true,
                            textHour: `${i}:00`,
                        }
                        hours.push(hourObject);
                    }

                    return {
                        ...day,
                        hours: hours,
                        start: startValue,
                        endValue: endValue,
                        // singleDateTime: singleDateTime.toISOString(),
                    };
                });
                // swiperTermsCalendar.update();
            } else {
                this.showCalendar = false;
            }
        }
    };
}