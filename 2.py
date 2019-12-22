from abc import abstractmethod
from operator import attrgetter


class Request:
    @classmethod
    @abstractmethod
    def from_string(cls, string: str):
        pass


class Appoint(Request):
    def __init__(self, day: int, hour: int, minute: int, duration: int, names: tuple):
        self._day = day
        self._hour = hour
        self._minute = minute
        self._duration = duration
        self._names = names

        self._start = day * 24 * 60 + hour * 60 + minute
        self._end = self._start + duration

    def intersection(self, other: "Appoint") -> frozenset:
        if other._end <= self._start or self._end <= other._start:
            return frozenset()
        else:
            return frozenset(self._names).intersection(frozenset(other._names))

    def is_participant(self, name: str) -> bool:
        return name in self._names

    @classmethod
    def from_string(cls, string: str) -> "Appoint":
        params = string.split()
        day = int(params[1])
        hour, minute = (int(i) for i in params[2].split(":"))
        duration = int(params[3])
        names = tuple(params[5:])
        return cls(day, hour, minute, duration, names)

    @property
    def day(self):
        return self._day

    @property
    def hour(self):
        return self._hour

    @property
    def minute(self):
        return self._minute

    @property
    def duration(self):
        return self._duration

    @property
    def names(self):
        return self._names


class Print(Request):
    def __init__(self, day: int, name: str):
        self._day = day
        self._name = name

    @classmethod
    def from_string(cls, string: str) -> "Print":
        params = string.split()
        day = int(params[1])
        name = params[2]
        return cls(day, name)

    @property
    def day(self):
        return self._day

    @property
    def name(self):
        return self._name


if __name__ == '__main__':
    n = int(input())
    appoint_requests = []
    responses = []
    for i in range(n):
        string = input()
        if string.startswith("APPOINT"):
            new_appoint_request = Appoint.from_string(string)

            intersected_names = set()
            for request in appoint_requests:
                intersected_names = intersected_names.union(request.intersection(new_appoint_request))

            if not intersected_names:
                responses.append("OK")
                appoint_requests.append(new_appoint_request)
            else:
                responses.append("FAIL\n" + " ".join(
                    name for name in new_appoint_request.names if name in intersected_names))

        elif string.startswith("PRINT"):
            request = Print.from_string(string)
            same_day_meetings = sorted((meeting for meeting in appoint_requests if meeting.day == request.day and
                                        meeting.is_participant(request.name)),
                                       key=attrgetter("_start"))
            if same_day_meetings:
                responses.append("\n".join(" ".join((f"{str(meeting.hour).zfill(2)}:{str(meeting.minute).zfill(2)}",
                                                     str(meeting.duration)) + meeting.names)
                                           for meeting in same_day_meetings))
        else:
            print("Bad request")

    for response in responses:
        print(response)
