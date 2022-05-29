function appData() {
    const baseUrl = window.location.origin;


    return {
        name: "",
        doctors: [],
        selectedDoctorId: '',
        selectedDoctor: {},
        showCalendar: false,
        shiftsDays: [],
        selectedTermDataTime: '',

        setName: function (name) {
            this.name = name;
        },

        init() {
            fetch(`${baseUrl}/api/test.json`)
                .then((response) => response.json())
                .then((json) => this.doctors = json);
        },

        filterDoctor() {
            this.selectedTermDataTime = '';
         
            if (this.selectedDoctorId) {
                this.showCalendar = true;
                console.log('filterDoctor');
                this.selectedDoctor = this.doctors.find(doctor => {
                    return doctor.id == this.selectedDoctorId;
                });

                this.shiftsDays = this.selectedDoctor.doctorshifts.map((day) => {
                    const startValue = parseInt(day.shiftStartTime.split(":")[0].replace(/^0+/, ''));
                    const endValue = parseInt(day.shiftEndTime.split(":")[0].replace(/^0+/, ''));
                    
                    const hours = [];
                    const plannedVisitsTerms = this.selectedDoctor.visits.map((item) => {
                        const dateZoneString = item.date.split("Z")[0];
                        const dateTimeObject = new Date(dateZoneString);

                        return dateTimeObject.toLocaleString();
                    });

                    console.log('plannedVisitsTerms', plannedVisitsTerms);

                    for (let i = startValue; i <= endValue; i++) {
                        let prefix = '';
                        if (i < 10) {
                            prefix = '0';
                        } 

                        const singleDateTime = new Date(`${day.date}T${prefix}${i}:00:00`);
                        // const singleDateTime = new Date(`${day.date}T12:00:00`);
                        const isReserved = plannedVisitsTerms.includes(singleDateTime.toLocaleString());


                        const hourObject = {
                            singleDateTime: singleDateTime.toLocaleString(),
                            isReserved: isReserved,
                            textHour: `${i}:00`,
                        };
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
        },
        checkVisitsExists() {
            if (this.selectedDoctor.visits) {
                return true;
            } else {
                return false;
            }
        }
    };
}