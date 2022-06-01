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
        selectedTermDataTimeISO: '',

        async init() {
            await fetch(`${baseUrl}/api/test.json`)
                .then((response) => response.json())
                .then((json) => this.doctors = json)
                .catch((error) => {
                    console.log(error);
                });

            await this.$nextTick(() => {
                const autoSelectedOptionOneOption = document.querySelector(".js-doctor-select option[selected]");

                // auto select doctor with option attribute 'selected'
                if (autoSelectedOptionOneOption) {
                    this.selectedDoctorId = autoSelectedOptionOneOption.value;
                    this.filterDoctor();
                }
            });
        },

        filterDoctor() {
            this.selectedTermDataTime = '';
            this.selectedTermDataTimeISO = '';

            const currentDateTimeStamp = new Date().setHours(0,0,0,0);

            if (this.selectedDoctorId) {
                this.showCalendar = true;
                this.selectedDoctor = this.doctors.find(doctor => {
                    return doctor.id == this.selectedDoctorId;
                });

                this.shiftsDays = this.selectedDoctor.doctorshifts.map((day) => {
                    // get int value from hour
                    const startValue = parseInt(day.shiftStartTime.split(":")[0].replace(/^0+/, ''));
                    const endValue = parseInt(day.shiftEndTime.split(":")[0].replace(/^0+/, ''));

                    const hours = [];
                    const plannedVisitsTerms = this.selectedDoctor.visits.map((item) => {
                        const dateZoneString = item.date.split("Z")[0];
                        const dateTimeObject = new Date(dateZoneString);

                        return dateTimeObject.toLocaleString();
                    });
                    // console.log('plannedVisitsTerms', plannedVisitsTerms);
                    // create hours items based on range start and end
                    for (let i = startValue; i < endValue; i++) {
                        let prefix = '';
                        if (i < 10) {
                            prefix = '0';
                        }

                        const singleDateTime = new Date(`${day.date}T${prefix}${i}:00:00`);
                        // const singleDateTime = new Date(`${day.date}T12:00:00`);
                        const isReserved = plannedVisitsTerms.includes(singleDateTime.toLocaleString());

                        const hourObject = {
                            singleDateTime: singleDateTime.toLocaleString(),
                            singleDateTimeISO: singleDateTime.toISOString(),
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
                // filter only today or future dates
                this.shiftsDays = this.shiftsDays.filter((shift) => {
                    const shiftDateTimeStamp = new Date(shift.date).setHours(0,0,0,0);

                    return shiftDateTimeStamp >= currentDateTimeStamp;
                });
                // sort by date
                this.shiftsDays.sort((a, b) => {
                    const aDate = new Date(a.date).setHours(0,0,0,0);
                    const bDate = new Date(b.date).setHours(0,0,0,0);

                    return aDate - bDate;
                });


            } else {
                this.showCalendar = false;
            }
        },
        checkVisitsExists() {
            if (this.selectedDoctor.doctorshifts && this.selectedDoctor.doctorshifts.length) {
                return true;
            } else {
                return false;
            }
        },
        handleSelectTime(dateTime, dateTimeISO) {
            this.selectedTermDataTime = dateTime;
            this.selectedTermDataTimeISO = dateTimeISO;
        },
    };
}