class CrewMember:
    def __init__(self, crew_id, name, role, assigned_flights):
        self.crew_id = crew_id
        self.name = name
        self.role = role
        self.assigned_flights = assigned_flights

    def assign_flight(self, flight):
        self.assigned_flights.append(flight)

    def remove_from_flight(self, flight):
        if flight in self.assigned_flights:
            self.assigned_flights.remove(flight)


class LoyaltyProgram:
    def __init__(self, loyalty_id, passenger, points, membership_level):
        self.loyalty_id = loyalty_id
        self.passenger = passenger
        self.points = points
        self.membership_level = membership_level

    def add_points(self, amount):
        self.points += amount

    def redeem_points(self, points):
        if points <= self.points:
            self.points -= points
            return True
        return False
