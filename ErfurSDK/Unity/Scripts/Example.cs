using System.Collections;
using UnityEngine;
using ErfurSDK;

public class Example : MonoBehaviour
{
    private  IEnumerator Start()
    {
        ErfurAnalysisPackageManager.Initialize("http://127.0.0.1:5000/", "");
        yield return new WaitForSeconds(5f);
        ErfurAnalysisPackageManager.UpdateOrAddValue("Systemlanguage",Application.systemLanguage.ToString());
    }


    private void OnApplicationQuit()
    {
        ErfurAnalysisPackageManager.IncreaseOrAddValue("Playtime", Time.time);
    }
}