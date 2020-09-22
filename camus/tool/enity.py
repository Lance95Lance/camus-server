from utils.other_utils.third_party_util import IdNumber


class IdNumberEnity:
    def __init__(self, id: str):
        self.idNumber = IdNumber(id)
        self.area_id = self.idNumber.area_id
        self.area_name = self.idNumber.get_area_name()
        self.birthday = self.idNumber.get_birthday()
        self.age = self.idNumber.get_age()
        self.sex = '男' if self.idNumber.get_sex() == 1 else '女'
        self.check_digit = self.idNumber.get_check_digit()
        self.facticity = '有效' if self.idNumber.verify_id(id) is True else '无效'

