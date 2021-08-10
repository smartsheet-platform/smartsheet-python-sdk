#!/usr/bin/env sh

MAIN_CLASS='com.github.tomakehurst.wiremock.standalone.WireMockServerRunner'

EXTENSION='ApiScenarioTransformer'

PORT=8082

export JDK_JAVA_OPTIONS='--add-modules java.xml.bind'

# launch wiremock
java  -cp "libs/*" $MAIN_CLASS --extensions=$EXTENSION --port=$PORT
