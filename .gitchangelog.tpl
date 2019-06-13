% for version in data["versions"]:
<%
title = "[%s] - %s" % (version["tag"], version["date"]) if version["tag"] else opts["unreleased_version_label"]
nb_sections = len(version["sections"])
%>${"## " + title}
% for section in version["sections"]:
${"### " + section["label"]}
% for commit in section["commits"]:
<%
subject = "%s" % (commit["subject"])
entry = indent('\n'.join(textwrap.wrap(subject)),
                       first="- ").strip()
%>${entry}
% endfor

% endfor
% endfor