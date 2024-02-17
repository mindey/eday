import unittest
import datetime
import eday

class TestEdays(unittest.TestCase):
    def test_from_date(self):
        # Test conversion from ISO format string
        self.assertAlmostEqual(eday.from_date('2022-02-17'), 19040.0, places=4)

        # Test conversion from datetime object
        dt = datetime.datetime(2022, 2, 17, 12, 0, 0)
        self.assertAlmostEqual(eday.from_date(dt), 19040.5, places=4)

    def test_to_date(self):
        # Test conversion to datetime object
        dt = eday.to_date(18864.5)
        self.assertEqual(dt.year, 2021)
        self.assertEqual(dt.month, 8)
        self.assertEqual(dt.day, 25)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)

    def test_now(self):
        # Test current UTC time
        now_eday = eday.now()
        dt = eday.to_date(now_eday)
        current_utc = datetime.datetime.utcnow()
        self.assertAlmostEqual(now_eday, eday.from_date(current_utc), places=4)
        self.assertAlmostEqual(dt, current_utc.replace(tzinfo=datetime.timezone.utc), delta=datetime.timedelta(seconds=1))

if __name__ == '__main__':
    unittest.main()
