using System.Collections;
using System.Collections.Generic;
using UnityEngine;

enum SampleType
{
    RGB, Depth, Transform, MovementMatrix
}

public class SceneGenerator : MonoBehaviour {
    public Move cameraMove;
    public GameObject[] samples;
    List<GameObject> pool = new List<GameObject>();
    public float SceneScale = 25;
    public Light mainLight;
    public int MinObjects;
    public int MaxObjects;
    // Use this for initialization
    void Start () {
		
	}
	
    void SpawnObjects()
    {
        foreach(GameObject g in pool)
        {
            g.SetActive(false);
        }

        mainLight.transform.eulerAngles = Random.insideUnitSphere * 180;
        cameraMove.GetComponent<Camera>().backgroundColor = Random.ColorHSV();
        cameraMove.transform.eulerAngles = new Vector3(Random.Range(-25f, 25f), Random.Range(-25f, 25f), Random.Range(-25f, 25f));
        cameraMove.direction = Random.insideUnitSphere * Random.Range(5f, 30f);
        mainLight.color = Random.ColorHSV();
        int objectsCount = Random.Range(MinObjects, MaxObjects);
        for(int i=0; i<objectsCount; i++)
        {
            Move obj;

            if(i< pool.Count - 1)
            {
                obj = pool[i].GetComponent<Move>();
            }
            else
            {
                obj = Instantiate(samples[Random.Range(0, samples.Length-1)]).GetComponent<Move>();
                pool.Add(obj.gameObject);
            }

            obj.gameObject.SetActive(true);

            obj.direction = Random.insideUnitSphere * Random.Range(0f, 10f);

            obj.GetComponent<MeshRenderer>().material.mainTexture = generateRandomTexture(25);
            obj.GetComponent<MeshRenderer>().material.color = Random.ColorHSV();
            obj.transform.localScale = Random.insideUnitSphere * SceneScale;
            obj.transform.localEulerAngles = Random.insideUnitSphere;
            obj.transform.position = Random.insideUnitSphere * SceneScale;
        }
    }

    Texture2D generateRandomTexture(int size)
    {
        Texture2D tex = new Texture2D(size, size);
        Color[] colors = new Color[size * size];
        for(int i=0; i<colors.Length; i++)
        {
            colors[i] = Random.ColorHSV();
        }
        tex.SetPixels(colors);
        tex.Apply();
        return tex;
    }

    public int Generate = 0;
    // Update is called once per frame
    public int frames = 2;
    public int currentFrame = 0;
    public int current_id = 0;
    public bool firstgen = true;

    void Update () {
        
        if (Generate>0)
        {
            cameraMove.ManualUpdate();

            if (firstgen)
            {
                SpawnObjects();
                currentFrame = frames;
                firstgen = false;
            }
            else
            {
                SaveScreen(current_id, SampleType.RGB);
                SaveScreen(current_id, SampleType.Depth);
            }

            foreach (GameObject o in pool)
                o.GetComponent<Move>().ManualUpdate();

            if (currentFrame > 0)
            {
                currentFrame -= 1;
            }
            else
            {
                firstgen = true;
                Generate--;
                current_id += 1;
            }
        }
	}

    public RenderTexture CameraRT;
    public RenderTexture DepthCameraRT;
    public Texture2D screenshot;
    void SaveScreen(int id, SampleType type=SampleType.RGB)
    {
        //yield return new WaitForEndOfFrame();
        // assumes you have your RenderTexture renderTexture
        screenshot = new Texture2D(CameraRT.width, CameraRT.height, TextureFormat.RGB24, false);
        if (type == SampleType.RGB)
            RenderTexture.active = CameraRT;
        else
            RenderTexture.active = DepthCameraRT;
        screenshot.ReadPixels(new Rect(0, 0, CameraRT.width, CameraRT.height), 0, 0);
        screenshot.Apply();

        byte[] bytes = screenshot.EncodeToPNG();
        Object.Destroy(screenshot);
        
        System.IO.Directory.CreateDirectory(System.IO.Directory.GetCurrentDirectory() + "/Dataset/rgb/" + id);
        System.IO.Directory.CreateDirectory(System.IO.Directory.GetCurrentDirectory() + "/Dataset/depth/" + id);

        // For testing purposes, also write to a file in the project folder
        if (type == SampleType.RGB)
            System.IO.File.WriteAllBytes(System.IO.Directory.GetCurrentDirectory() + "/Dataset/rgb/" + id + "/sc_" + currentFrame + ".png", bytes);
        else
            System.IO.File.WriteAllBytes(System.IO.Directory.GetCurrentDirectory() + "/Dataset/depth/" + id + "/sc_" + currentFrame + ".png", bytes);
    }
}
