class Flight:
   def __init__(self, flight_id, airline, source, destination, departure_time, arrival_time, available_seats):
        self.flight_id = flight_id
        self.airline = airline
        self.source = source
        self.destination = destination
        self.departure_time = departure_time
        self.arrival_time = arrival_time
        self.available_seats = available_seats

    def update_flight_schedule(self, new_time):
        self.departure_time = new_time

    def check_availability(self):
        return self.available_seats > 0

    def get_flight_info(self):
        return (f"Flight ID: {self.flight_id}, Airline: {self.airline}, Source: {self.source}, "
                f"Destination: {self.destination}, Departure Time: {self.departure_time}, "
                f"Arrival Time: {self.arrival_time}, Available Seats: {self.available_seats}")
class Ticket:
    def __init__(self, ticket_id, passenger, flight, seat_number, ticket_class, price, status):
        self.ticket_id = ticket_id
        self.passenger = passenger
        self.flight = flight
        self.seat_number = seat_number
        self.ticket_class = ticket_class
        self.price = price
        self.status = status

    def generate_ticket(self):
        return (f"Ticket ID: {self.ticket_id}, Passenger: {self.passenger}, Flight: {self.flight.get_flight_info()}, "
                f"Seat Number: {self.seat_number}, Class: {self.ticket_class}, Price: {self.price}, Status: {self.status}")

    def cancel_ticket(self):
        self.status = "Cancelled"
        self.flight.available_seats += 1

    def change_seat(self, new_seat):
        self.seat_number = new_seat


class Booking:
    def __init__(self, booking_id, passenger, flight, ticket, status):
        self.booking_id = booking_id
        self.passenger = passenger
        self.flight = flight
        self.ticket = ticket
        self.status = status

    def confirm_booking(self):
        self.status = "Confirmed"

    def cancel_booking(self):
        self.status = "Cancelled"
        self.ticket.cancel_ticket()

    def modify_booking(self, new_flight):
        self.flight = new_flight
        self.ticket.flight = new_flight

#class FlightReminder(Flight):
    #def check_reminder(self):
        #now = datetime.now()
        #time_until = self.departure_time - now
        #if time_until <= timedelta(hours=3):
            #try:
                #back to payment class, would change the names depending on how it will be named there - Check if Payment class exists and payment is done
                #if Payment.is_payment_done(self.flight_id):
                    #print(f"Reminder: Only {time_until} left until flight {self.flight_id} departure!")
                #else:
                   # print("There's no Reminder for you, please check your payment" )
