from sensors import ConvoTrap, ScaleBait, PhishPuppet


def test_sensors_start_stop():
    c = ConvoTrap()
    s = ScaleBait()
    p = PhishPuppet()

    assert c.start() == "convotrap started"
    assert c.running is True
    assert c.stop() == "convotrap stopped"
    assert c.running is False

    assert s.start() == "scalebait started"
    assert s.running is True
    assert s.stop() == "scalebait stopped"
    assert s.running is False

    assert p.start() == "phishpuppet started"
    assert p.running is True
    assert p.stop() == "phishpuppet stopped"
    assert p.running is False
