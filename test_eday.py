import unittest
import datetime
import eday

class TestEdays(unittest.TestCase):

    def test_from_date(self):
        # Test conversion from ISO format string
        self.assertAlmostEqual(eday.from_date('2022-02-17'), 19040.0, places=6)

        # Test conversion from datetime object
        dt = datetime.datetime(2022, 2, 17, 12, 0, 0)
        self.assertAlmostEqual(eday.from_date(dt), 19040.5, places=6)

        # Test conversion from date string with time
        self.assertAlmostEqual(eday.from_date('2022-02-17T12:00:00+00:00'), 19040.5, places=6)

        # Test conversion from negative time expression
        self.assertAlmostEqual(eday.from_date('-12:00'), -0.5, places=6)

        # Test conversion from mixed time expression
        self.assertAlmostEqual(eday.from_date('25:50'), 1.0763888888888888, places=6)

    def test_to_date(self):
        # Test conversion to datetime object
        dt = eday.to_date(18864.5)
        self.assertEqual(dt.year, 2021)
        self.assertEqual(dt.month, 8)
        self.assertEqual(dt.day, 25)
        self.assertEqual(dt.hour, 12)
        self.assertEqual(dt.minute, 0)
        self.assertEqual(dt.second, 0)

        # Test conversion for edge case value
        dt = eday.to_date(-719162.0)
        self.assertEqual(dt.year, 1)
        self.assertEqual(dt.month, 1)
        self.assertEqual(dt.day, 1)

        dt = eday.to_date(2932896.0)
        self.assertEqual(dt.year, 9999)
        self.assertEqual(dt.month, 12)
        self.assertEqual(dt.day, 31)

    def test_now(self):
        # Test current UTC time
        now_eday = eday.now()
        dt = eday.to_date(now_eday)
        current_utc = datetime.datetime.utcnow()
        self.assertAlmostEqual(now_eday, eday.from_date(current_utc), places=6)
        self.assertAlmostEqual(dt, current_utc.replace(tzinfo=datetime.timezone.utc), delta=datetime.timedelta(seconds=1))

    def test_addition(self):
        eday1 = eday('2022-02-17')
        eday2 = eday('2022-02-18')
        self.assertAlmostEqual((eday1 + 1), eday2, places=6)
        self.assertAlmostEqual((eday1 + eday2), eday(19040.0 + 19041.0), places=6)

    def test_subtraction(self):
        eday1 = eday('2022-02-18')
        eday2 = eday('2022-02-17')
        self.assertAlmostEqual((eday1 - 1), eday2, places=6)
        self.assertAlmostEqual((eday1 - eday2), eday(1.0), places=6)

    def test_repr(self):
        # Test representation of Eday object
        eday_obj = eday('2022-02-17')
        self.assertEqual(repr(eday_obj), '19040.0 <2022-02-17 00:00:00+00:00>')

if __name__ == '__main__':
    unittest.main()
