import csv
from StringIO import StringIO


def csv_res2_dict_lst(res):
    """Convert CSV string with a header into list of dictionaries"""
    return list(csv.DictReader(StringIO(res), delimiter=","))


def expected_repnames(repos_cfg):
    """Generate expected repository names '{account_name}/{repo_name}'"""
    templ = "{account_name}/{repo_name}"
    lst = []
    for account_name, rep_cfg in repos_cfg.items():
        for repo_name in rep_cfg.keys():
            lst.append(
                templ.format(account_name=account_name, repo_name=repo_name)
            )
    return sorted(lst)


def test_simple_call(binbb):
    # Just try to run it and hope it will not fail
    binbb.sysexec("repo", "list")
    binbb.sysexec("repo", "list", "-f", "csv")
    binbb.sysexec("repo", "list", "-f", "value")
    binbb.sysexec("repo", "list", "-c", "Owner", "-c", "Repo Name")
    binbb.sysexec("repo", "list", "-c", "Owner", "-c", "Repo Name", "-f", "csv")


def test_listed_names_csv(binbb, repos_cfg):
    res = binbb.sysexec("repo", "list", "-f", "csv")
    recs = csv_res2_dict_lst(res)
    resnames = ["{rec[Owner]}/{rec[Repo Name]}".format(rec=rec) for rec in recs]
    resnames = sorted(resnames)
    expected = expected_repnames(repos_cfg)
    assert resnames == expected


def test_listed_names_value(binbb, repos_cfg):
    # Just try to run it and hope it will not fail
    bbcmd = ["repo", "list", "-f", "value", "-c" "Owner", "-c", "Repo Name"]
    res = binbb.sysexec(*bbcmd)
    recs = res.strip().splitlines()
    recs = [line.split(" ", 1) for line in recs]
    templ = "{owner}/{repo}"
    resnames = [templ.format(owner=owner, repo=repo) for owner, repo in recs]
    resnames = sorted(resnames)
    expected = expected_repnames(repos_cfg)
    assert resnames == expected
