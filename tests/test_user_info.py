import subprocess


def test_it(binbb, account):
    """Test just the first one"""
    expected_words = ("Fields Value username first_name last_name display_name"
                      "is_team is_staff").split()
    bbcmd = ["user", "info"]
    # Expecting the call to succeed
    #res = binbb.sysexec(*bbcmd)
    cmd = [binbb.strpath] + bbcmd
    res = subprocess.check_output(cmd)

    # Make simple test if the output is as expected
    for word in expected_words:
        assert word in res
    lines = res.strip().splitlines()
    assert len(lines) >= 10
