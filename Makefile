ZIP_FILENAME="package.zip"
TARGET_DIRNAME="pkg"
IGNORE_FILES=".gitkeep"

ZIP_FILEPATH="../${ZIP_FILENAME}"

main: clean zip remove-files remove-caches

clean:
	cd ${TARGET_DIRNAME} && rm ${ZIP_FILEPATH} || true

zip:
	cd ${TARGET_DIRNAME} && zip -r ${ZIP_FILEPATH} *

remove-files:
	zip -d ${ZIP_FILENAME} ${TARGET_DIRNAME}/${IGNORE_FILES} || true

remove-caches:
	find ${TARGET_DIRNAME} -type d -name "__pycache__" \
	| sed 's/^pkg\///g' \
	| xargs -I{} zip -d ${ZIP_FILENAME} {}/*
