def test_it(binbb, repos_cfg):
    """Test just the first one"""
    expected_words = ("Fields Values Branch Name Author"
                      " TimeStamp Commit ID Message").split()
    for account_name, rep_cfg in repos_cfg.items():
        for repo_name in rep_cfg.keys():
            bbcmd = ["repo", "branch", "-a", account_name, "-r", repo_name]
            # Expecting the call to succeed
            res = binbb.sysexec(*bbcmd)

            # Make simple test if the output is as expected
            for word in expected_words:
                assert word in res
            lines = res.strip().splitlines()
            assert len(lines) >= 8

            # Stop testing with first repository
            return
