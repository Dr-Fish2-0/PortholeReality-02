using UnityEngine;

public class EditProjectionMatrix : MonoBehaviour
{
    Camera currentCamera;

    [Header("Window Properties")]
    [SerializeField] float windowHeight;
    [SerializeField] float windowWidth;
    [SerializeField] GameObject followObject;
    [SerializeField] Vector3 offset;
    [SerializeField] Transform windowCenter;
    [SerializeField] SocketTest positionTracker;
    [SerializeField] Transform stereoCamTransform;

    [Header("Projection Matrix")]
    [SerializeField] bool isEditable;
    [SerializeField] Matrix4x4 editedProjectionMatrix;

    private float verticalAdjustment;
    private float horizontalAdjustment; 

    Vector3 playerPosition;

    // Start is called once before the first execution of Update after the MonoBehaviour is created
    void Start()
    {
        currentCamera = GetComponent<Camera>();

        verticalAdjustment = 0.03f;
        horizontalAdjustment = 0.09f;

        editedProjectionMatrix = currentCamera.projectionMatrix;
    }

    // Update is called once per frame
    void Update()
    {
        //transform.localPosition = followObject.transform.localPosition+offset;
        //currentCamera.nearClipPlane = Vector3.Distance(transform.position, windowCenter.position);

        playerPosition = positionTracker.recPosition;

        playerPosition = stereoCamTransform.transform.TransformPoint(playerPosition);
        
        playerPosition = windowCenter.InverseTransformPoint(playerPosition);
        playerPosition.z = -(playerPosition.z+0.03f);
        playerPosition.y = playerPosition.y-0.09f;

        if (Input.GetKeyDown(KeyCode.DownArrow)) verticalAdjustment -= 0.001f;
        if (Input.GetKeyDown(KeyCode.UpArrow)) verticalAdjustment += 0.001f;

        if (Input.GetKeyDown(KeyCode.S)) horizontalAdjustment -= 0.001f;
        if (Input.GetKeyDown(KeyCode.W)) horizontalAdjustment += 0.001f;

        transform.localPosition = Vector3.Lerp(transform.localPosition, playerPosition, Time.deltaTime*4);

        if (!isEditable)
        {
            editedProjectionMatrix.m00 = -(transform.localPosition.z / windowWidth);
            editedProjectionMatrix.m11 = -(transform.localPosition.z / windowHeight);

            editedProjectionMatrix.m02 = -(transform.localPosition.x / windowWidth);
            editedProjectionMatrix.m12 = -(transform.localPosition.y / windowHeight);
        }
        currentCamera.projectionMatrix = editedProjectionMatrix;
    }
}
