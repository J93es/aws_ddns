import copy
from record import Records

class Each_Hosted_Zone_Distinction:
    name: str
    comment: str | None
    
    def __init__(self, name: str, comment: str | None) -> None:
        self.name = str(name).strip()
        self.comment = str(comment).strip() if comment is not None else None
    
    def __eq__(self, other) -> bool:
        is_name_same = self.name == other.to_dict()['Name']
        is_comment_same = self.comment == other.to_dict()['Comment'] or self.comment is None
        return is_name_same and is_comment_same
    
    def to_dict(self) -> dict:
        return {
            'Name' : self.name,
            'Comment' : self.comment,
        }

        

class Each_Hosted_Zone:
    id: str
    name: str
    comment: str | None
    distinction: Each_Hosted_Zone_Distinction
    records: Records
    
    def __init__(self, each_hosted_zone: dict) -> None:
        if isinstance(each_hosted_zone, Each_Hosted_Zone):
            self.id = str(self.id).strip()
            self.name = str(self.name).strip()
            self.comment = str(self.comment).strip() if self.comment is not None else None
            self.distinction = Each_Hosted_Zone_Distinction(self.name, self.comment)
            self.records = Records(self.records)
            return 
            
        self.id = str(each_hosted_zone['Id']).strip()
        self.name = str(each_hosted_zone['Name']).strip()
        self.comment = str(each_hosted_zone['Comment']).strip() if each_hosted_zone['Comment'] is not None else None
        self.distinction = Each_Hosted_Zone_Distinction(self.name, self.comment)
        self.records = Records(each_hosted_zone['Records'])
        
    
    def __eq__(self, value: object) -> bool:
        return self.distinction == value.get_distinction()
    
    def to_dict(self) -> dict:
        return {
            'Id' : self.id,
            'Name' : self.name,
            'Comment' : self.comment,
            'Distinction' : self.distinction.to_dict(),
            'Records' : self.records.to_list(),
        }
        
    def get_distinction(self) -> Each_Hosted_Zone_Distinction:
        return copy.deepcopy(self.distinction)
    
    def get_records(self) -> Records:
        return copy.deepcopy(self.records)
        
        
class Hosted_Zones:
    hosted_zones: list
    
    def __init__(self, hosted_zones: list) -> None:
        if isinstance(hosted_zones, Hosted_Zones):
            self.hosted_zones = hosted_zones.hosted_zones.to_list()
            return
        
        self.hosted_zones = []
        for each_hosted_zone in hosted_zones:
            self.hosted_zones.append(Each_Hosted_Zone(each_hosted_zone))
            
    def __iter__(self):
        return iter(self.hosted_zones)
    
    def to_list(self) -> list:
        hosted_zones = []
        for hosted_zone in self.hosted_zones:
            hosted_zones.append(hosted_zone.to_dict())
        return hosted_zones
    
    def get_distinctions(self) -> list:
        distinctions = []
        for hosted_zone in self.hosted_zones:
            distinctions.append(hosted_zone.get_distinction())
        return distinctions
    
    def find_by_distinction(self, distinction: Each_Hosted_Zone_Distinction) -> Each_Hosted_Zone | None:
        for hosted_zone in self.hosted_zones:
            if hosted_zone.distinction == distinction:
                return hosted_zone
        return None
    
# a = Hosted_Zones([
#     {
#         "Name" : "example1.com",
#         "Comment" : "",
        
#         "Records" : [
#             {
#                 "Name" : "example1.com",
#                 "TTL": 300,
#                 "Resource": [
#                     {
#                         "Value": "val"
#                     }
#                 ],
#             },
#         ],
#     }]
# )

# print(a)