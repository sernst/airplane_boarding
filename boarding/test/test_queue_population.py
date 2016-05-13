import unittest

from boarding import configuration
from boarding.ops import passengers as passenger_ops
from boarding.ops import queue as queue_ops


class TestQueuePopulation(unittest.TestCase):

    def setUp(self):
        self.settings = configuration.load(dict(
            airplane=[{"rows": 2, "seats": [2, 2]}]
        ))
        self.passengers = passenger_ops.create(self.settings)

    def test_random(self):
        """
        """
        self.settings['populate'] = 'RANDOM'
        queue = queue_ops.populate(
            self.settings,
            queue_ops.create(self.settings, self.passengers),
            self.passengers
        )

    def test_random(self):
        """
        """
        self.settings['populate'] = {
            'type': 'RANDOM',
            'groups': 2
        }

        queue = queue_ops.populate(
            self.settings,
            queue_ops.create(self.settings, self.passengers),
            self.passengers
        )
        print('RANDOM [2 GROUPS]:')
        print(queue)

    def test_forward(self):
        """
        """
        self.settings['populate'] = 'FORWARD'
        queue = queue_ops.populate(
            self.settings,
            queue_ops.create(self.settings, self.passengers),
            self.passengers
        )

        print('FORWARD:')
        print(queue)

    def test_backward(self):
        """
        """
        self.settings['populate'] = 'BACKWARD'
        queue = queue_ops.populate(
            self.settings,
            queue_ops.create(self.settings, self.passengers),
            self.passengers
        )
        print('BACKWARD:')
        print(queue)

################################################################################
################################################################################

if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestQueuePopulation)
    unittest.TextTestRunner(verbosity=2).run(suite)




