test:
	flake8

install-precommit:
	echo '#!/bin/sh\ngit stash -q --keep-index\nmake test\nRESULT=$$?\ngit stash pop -q\nexit $$RESULT\n' > .git/hooks/pre-commit;
	chmod +x .git/hooks/pre-commit;
