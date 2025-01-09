using UnityEngine;

public class EditProjectionMatrix : MonoBehaviour
{
    Camera currentCamera;

    //These define important positions and dimensions for the window
    [Header("Window Properties")]
    [SerializeField] float windowHeight;
    [SerializeField] float windowWidth;
    [SerializeField] GameObject followObject;
    [SerializeField] Vector3 offset;
    [SerializeField] Transform windowCenter;
    [SerializeField] SocketTest positionTracker;
    [SerializeField] Transform stereoCamTransform;

    //Stores the projection Matrix
    [Header("Projection Matrix")]
    [SerializeField] bool isEditable;
    [SerializeField] Matrix4x4 editedProjectionMatrix;

    //Offsets for the camera
    private float verticalAdjustment;
    private float horizontalAdjustment; 

    Vector3 playerPosition;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        //Get the camera attached to this game object
        currentCamera = GetComponent<Camera>();

        //define the offsets for the players view
        verticalAdjustment = 0.03f;
        horizontalAdjustment = 0.09f;

        //get the current projection matrix
        editedProjectionMatrix = currentCamera.projectionMatrix;
    }

    // Update is called once per frame
    void Update()
    {
        //gets the viewers position relative to the camera
        playerPosition = positionTracker.recPosition;

        //transform the viewers position to world space
        playerPosition = stereoCamTransform.transform.TransformPoint(playerPosition);
        
        //transform the viewers position to coordinates realtive to the window
        //and add the offsets
        playerPosition = windowCenter.InverseTransformPoint(playerPosition);
        playerPosition.z = -(playerPosition.z+0.03f);
        playerPosition.y = playerPosition.y-0.09f;

        //This allows the viewer to adjust the offsets live
        if (Input.GetKeyDown(KeyCode.DownArrow)) verticalAdjustment -= 0.001f;
        if (Input.GetKeyDown(KeyCode.UpArrow)) verticalAdjustment += 0.001f;

        if (Input.GetKeyDown(KeyCode.S)) horizontalAdjustment -= 0.001f;
        if (Input.GetKeyDown(KeyCode.W)) horizontalAdjustment += 0.001f;

        //Smooth out the movement because the tracker adds jitter
        transform.localPosition = Vector3.Lerp(transform.localPosition, playerPosition, Time.deltaTime*4);

        //Four lines of arithmetic that get the right perspective
        if (!isEditable)
        {
            /*
             * w = window width
             * h = window height
             * 
             * -cot(z/w) 0          0      0
             * 0         -cot(z/h)  0      0
             * -x/w      -y/h       1      0
             * 0         0          0      1
             */
            editedProjectionMatrix.m00 = -(transform.localPosition.z / windowWidth);
            editedProjectionMatrix.m11 = -(transform.localPosition.z / windowHeight);

            editedProjectionMatrix.m02 = -(transform.localPosition.x / windowWidth);
            editedProjectionMatrix.m12 = -(transform.localPosition.y / windowHeight);
        }
        currentCamera.projectionMatrix = editedProjectionMatrix;
    }
}
