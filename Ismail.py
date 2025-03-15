class Airport:
    
    def __init__(self , airport_id , name , location , avilable_flights):

        self.airport_id = airport_id
        self.name = name
        self.location = location
        self.avilable_flights = avilable_flights

    def list_flights(self):

        print(f"Airport Id:  , {self.airport_id} \n"
                f"Name:  , {self.name}\n"
                f"Location:  , {self.location} \n"
                f"Avilable flights:  , {self.avilable_flights} \n"
                f"")

    def get_airport_info(self):

        return self.airport_id , self.name , self.location , self.avilable_flights #return the info is enought to make get info method

    def check_flight_status(self , fligh_id):
        pass
    


class Airline:
    
    def __init__(self , airline_id , name , fleet_size , destinations , customer_rating):

        self.airline_id = airline_id
        self.name = name
        self.fleet_size = fleet_size
        self.destinations = destinations
        self.customer_rating = customer_rating

    def list_flights_by_airline(self):
        
        print(f"Airline Id: {self.airline_id} \n"
              f"Name: {self.name} \n"
              f"Fleet size: {self.fleet_size} \n"
              f"Destinations: {self.destinations}"
              f"Customer Rating: {self.customer_rating}"
              f"")

    def get_airline_info(self):
            
        return self.airline_id , self.name , self.fleet_size , self.destination , self.customer_rating #return the info is enought to make get info method

    #how about using if conditions for every update data and print all the data with the changed one??
    def update_airline_details(self): 
         pass

class Payment:
    
    def __init__(self, payment_id, passenger, amount, payment_method, status):

        self.payment_id = payment_id
        self.passenger = passenger
        self.amount = amount
        self.payment_method = payment_method
        self.status = status

    def process_payment(self):
        pass

    def refund_payment(self):
        pass

    def view_payment_history(self):
        
        #if all of the data got changed due to a new payment, it will be printed and be saved
        if self.payment_id and self.passenger and self.amount and self.payment_method and self.status:

            print(f"Payment Id: {self.payment_id} \n"
                  f"Passenger: {self.passenger} \n"
                  f"Amount: {self.amount} \n"
                  f"Payment Method: {self.payment_method} \n"
                  f"Status: {self.status}"
                  f"")