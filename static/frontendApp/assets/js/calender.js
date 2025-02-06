document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
      schedulerLicenseKey: 'GPL-My-Project-Is-Open-Source',
      expandRows: true,
     
      headerToolbar: {
        left: 'title today prev,next',
        right: 'dayGridMonth,timeGridWeek,timeGridDay' 
      },
      initialView: 'dayGridMonth',
      initialDate: '2024-06-01',
      allDaySlot: false,       
      businessHours: {
      daysOfWeek: [ 1, 2, 3, 4, 5, 6 ], // Monday - Saturday
      startTime: '00:00',
      endTime: '24:00',
    },
      events: [
       
        {
          title: 'Conference',
          start: '2024-06-05T09:00:00',
          end:'2024-06-05T10:00:00',
          backgroundColor: '#FFEDD5',
          textColor: '#111827',
        },
        {
            title: 'Upload Doc',
            start: '2024-06-05T11:30:00',
            end:'2024-06-05T12:00:00',
            backgroundColor: '#CFFAFE',
            textColor: '#111827',
        },
        {
          title: 'Kate Feedback',
          start: '2024-06-06T08:00:00',
          end:'2024-06-06T08:30:00',
          backgroundColor: '#EFF6FF',
          textColor: '#111827',
        },
        {
          title: 'Meet With Smith',
          start: '2024-06-06T10:00:00',
          end:'2024-06-06T11:00:00',
          backgroundColor: '#E0F2FE',
          textColor: '#111827',
        },
        {
          title: 'Update Design Systeam',
          start: '2024-06-07T08:30:00',
          end:'2024-06-07T07:30:00',
          backgroundColor: '#ECFCCB',
          textColor: '#111827',
        },
        {
          title: 'Upload Doc',
          start: '2024-06-07T09:30:00',
          end:'2024-06-07T10:00:00',
          backgroundColor: '#CFFAFE',
          textColor: '#111827',
        },
        {
          title: 'Meet With Smith',
          start: '2024-06-08T09:00:00',
          end:'2024-06-08T10:00:00',
          backgroundColor: '#E0F2FE',
          textColor: '#111827',
        },
        {
          title: 'Daily Sync',
          start: '2024-06-08T11:00:00',
          end:'2024-06-08T12:30:00',
          backgroundColor: '#EDE9FE',
          textColor: '#111827',
        },
        {
          title: 'Meet With Smith',
          start: '2024-06-13T12:30:00',
          end:'2024-06-13T13:00:00',
          backgroundColor: '#E0F2FE',
          textColor: '#111827',
        },
        {
          title: 'Kate Feedback',
          start: '2024-06-12T08:30:00',
          end:'2024-06-12T08:30:00',
          backgroundColor: '#EFF6FF',
          textColor: '#111827',
        },
        {
          title: 'Upload Doc',
          start: '2024-06-12T10:30:00',
          end:'2024-06-12T11:00:00',
          backgroundColor: '#CFFAFE',
          textColor: '#111827',
        },
        {
          title: 'Daily Sync',
          start: '2024-06-10T08:00:00',
          end:'2024-06-10T09:00:00',
          backgroundColor: '#CFFAFE',
          textColor: '#111827',
        },
        {
        title: 'Upload Report',
        start: '2024-06-10T09:00:00',
        end:'2024-06-10T10:00:00',
        backgroundColor: '#EDE9FE',
        textColor: '#111827',
      },
      {
        title: 'Update Design Systeam',
        start: '2024-06-11T11:00:00',
        end:'2024-06-10T11:00:00',
        backgroundColor: '#ECFCCB',
        textColor: '#111827',
      },
      ]
    });

    calendar.render();
  });