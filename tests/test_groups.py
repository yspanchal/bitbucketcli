def test_it(binbb, groups_cfg):
    for account, accgrp_cfg in groups_cfg.items():
        bbcmd = ["groups", "--account", account]
        res = binbb.sysexec(*bbcmd)
        # very simple test of group names and member names being seen in output
        for group_name, members in accgrp_cfg.items():
            assert group_name in res
            for member_name in members:
                assert member_name in res
