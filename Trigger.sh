#!/bin/sh

python ./PreProcess.py
if [ $? -ne 0 ];then
    echo "Error : PreProcess.py Failed"
    exit 1
else
    echo "Info : PreProcess.py Ran Successfully"

    # Calling DQ FrameWork Standalone Version for $Rule_Set_Assignment

    python ./DQDummyStandalone.py

    if [ $? -ne 0 ];then
        echo "Error : DQ Failed"
        exit 1
    else
		# Calling DQReferenceDataSetup.py
		echo "Info : DQDummyStandalone.py ran successfully, calling DQReferenceDataSetup.py"
		python ./DQReferenceDataSetup.py
		if [ $? -ne 0 ];then
			echo "Error : ./DQReferenceDataSetup.py Failed"
			exit 1
		else
			# calling DQDummyPackaged.py
			echo "Info : DQReferenceDataSetup.py ran successfully, calling DQ_Dummy_Packaged.py"
			python ./DQDummyPackaged.py
			if [ $? -ne 0 ];then
				echo "Error : DQ_Dummy_Packaged.py Failed."
				exit 1
			else
				# Calling PostProcess.py
				echo "Info : DQReferenceDataSetup.py ran successfully, Calling PostProcess.py"
				python ./PostProcess.py
				if [ $? -ne 0 ];then
					echo "Error : PostProcess.py failed"
					exit 1
				else
					echo "Info : PostProcess.py ran successfully"
					# Running NotifyResuly.py

					python ./NotifyResult.py
					if [ $? -ne 0 ];then
						echo "Error : NotifyResult.py Failed"
						exit 1
					else
						echo "Info : NotifyResult.py Completed Successfully"
						echo "Info : Trigger.sh Completed Successfully"
						exit 0
					fi
				fi
			fi
		fi
	fi
fi