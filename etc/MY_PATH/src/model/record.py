import copy

class Each_Record_Distinction:
    name: str
    
    def __init__(self, name: str) -> None:
        self.name = str(name).strip()
    
    def __eq__(self, other) -> bool:
        return self.name == other.to_dict()['Name']
    
    def to_dict(self) -> dict:
        return {
            'Name' : self.name,
        }


class Each_Record:
    name: str
    ttl: int
    resource: list
    distinction: Each_Record_Distinction
    
    def __init__(self, each_record: dict) -> None:
        if isinstance(each_record, Each_Record):
            self.name = str(self.name).strip()
            self.ttl = int(self.ttl)
            self.resource = copy.deepcopy(self.resource)
            self.distinction = Each_Record_Distinction(self.name)
            return
        
        self.name = str(each_record['Name']).strip()
        self.ttl = int(each_record['TTL'])
        self.resource = copy.deepcopy(each_record['Resource'])
        self.distinction = Each_Record_Distinction(self.name)
    
    def __eq__(self, other) -> bool:
        return self.distinction == other.get_distinction()
    
    def to_dict(self) -> dict:
        return {
            'Name' : self.name,
            'TTL' : self.ttl,
            'Resource' : self.resource,
            'Distinction' : self.distinction.to_dict()
        }
        
    def get_distinction(self) -> Each_Record_Distinction:
        return copy.deepcopy(self.distinction)


class Records:
    records: list
    
    def __init__(self, records: list) -> None:
        if isinstance(records, Records):
            self.records = records.to_list()
            return
        
        self.records = []
        for each_record in records:
            if isinstance(each_record, Each_Record):
                self.records.append(each_record)
            else:
                self.records.append(Each_Record(each_record))
            
    def __iter__(self):
        return iter(self.records)
    
    def to_list(self) -> list:
        records = []
        for record in self.records:
            records.append(record.to_dict())
        return records
            
    def get_distinctions(self) -> list:
        Distinctions = []
        for record in self.records:
            Distinctions.append(record.get_distinction())
        return Distinctions
            
    def find_by_distinction(self, distinction: Each_Record_Distinction) -> Each_Record | None:
        for record in self.records:
            if record.get_distinction() == distinction:
                return record
        return None