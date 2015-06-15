def test_it(binbb, account):
    # test only for owner, other owner might give restrictions
    bbcmd = ["sshkey", "-a", account]
    # Expecting the call to succeed
    res = binbb.sysexec(*bbcmd)
    print res
